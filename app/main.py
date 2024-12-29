from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
from pathlib import Path
import json
import datetime
import subprocess
import sys
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt

app = FastAPI(title="Halal Compliance Monitoring API")

# Call verify_data_exists during startup
@app.on_event("startup")
async def startup_event():
    verify_data_exists()

def verify_data_exists():
    """Verify that all required data files and directories exist."""
    print(f"Starting data verification process...")
    
    # Create and set permissions for results directory
    os.makedirs('/app/results', exist_ok=True)
    os.chmod('/app/results', 0o777)
    print(f"Results directory created and permissions set")
    
    # Create visualization directories
    models = ['slaughterhouse', 'food_processing']
    dimensions = ['2d', '3d']
    for model in models:
        for dim in dimensions:
            viz_dir = VISUALIZATIONS_DIR / model / dim
            viz_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(str(viz_dir), 0o777)
            print(f"Created visualization directory: {viz_dir}")
    
    required_files = [
        RESULTS_DIR / "slaughterhouse_results.json",
        RESULTS_DIR / "food_processing_results.json"
    ]
    
    missing_files = [str(f) for f in required_files if not f.exists()]
    if missing_files or not any((VISUALIZATIONS_DIR / 'slaughterhouse' / '2d').glob('*.png')):
        print(f"Missing files or visualizations, regenerating data...")
        try:
            env = os.environ.copy()
            env['PYTHONPATH'] = str(Path(__file__).parent)
            result = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "generate_test_data.py")],
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            print(f"Data generation output: {result.stdout}")
            print("Data and visualization generation completed")
            
            # Verify visualization files were created
            for model in models:
                for dim in dimensions:
                    viz_path = VISUALIZATIONS_DIR / model / dim
                    files = list(viz_path.glob('*.png'))
                    print(f"Generated visualizations for {model}/{dim}: {len(files)} files")
        except subprocess.CalledProcessError as e:
            print(f"Error generating data: {e.stderr}")
            raise RuntimeError("Failed to generate required data files")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory for simulation results
RESULTS_DIR = Path("/app/results")
VISUALIZATIONS_DIR = RESULTS_DIR / "visualizations"

# Ensure directories exist
RESULTS_DIR.mkdir(exist_ok=True)
VISUALIZATIONS_DIR.mkdir(exist_ok=True, parents=True)

@app.get("/")
async def root():
    return {"message": "Halal Compliance Monitoring API"}

@app.get("/api/health")
async def health_check():
    try:
        # Check if data files exist
        slaughterhouse_exists = (RESULTS_DIR / "slaughterhouse_results.json").exists()
        food_processing_exists = (RESULTS_DIR / "food_processing_results.json").exists()
        
        return {
            "status": "healthy" if slaughterhouse_exists and food_processing_exists else "missing_data",
            "timestamp": datetime.datetime.now().isoformat(),
            "data_status": {
                "slaughterhouse_results": "present" if slaughterhouse_exists else "missing",
                "food_processing_results": "present" if food_processing_exists else "missing"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.datetime.now().isoformat(),
            "error": str(e)
        }

@app.get("/api/results")
async def get_results():
    try:
        # Load simulation results
        slaughterhouse_results = RESULTS_DIR / "slaughterhouse_results.json"
        food_processing_results = RESULTS_DIR / "food_processing_results.json"
        
        results = {
            "slaughterhouse": json.loads(slaughterhouse_results.read_text()) if slaughterhouse_results.exists() else {},
            "food_processing": json.loads(food_processing_results.read_text()) if food_processing_results.exists() else {}
        }
        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/results/slaughterhouse")
async def get_slaughterhouse_results():
    try:
        results_file = RESULTS_DIR / "slaughterhouse_results.json"
        if not results_file.exists():
            raise HTTPException(status_code=404, detail="Slaughterhouse results not found")
        return JSONResponse(content=json.loads(results_file.read_text()))
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Invalid JSON data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/results/food_processing")
async def get_food_processing_results():
    try:
        results_file = RESULTS_DIR / "food_processing_results.json"
        if not results_file.exists():
            raise HTTPException(status_code=404, detail="Food processing results not found")
        return JSONResponse(content=json.loads(results_file.read_text()))
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Invalid JSON data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/visualizations/{model}/{dimension}/{condition}")
async def get_visualization(model: str, dimension: str, condition: str):
    """Get pre-generated visualization file."""
    try:
        # Remove .png from condition if it's already there
        condition = condition.replace('.png', '')
        viz_path = VISUALIZATIONS_DIR / model / dimension / f"{condition}.png"
        
        if not viz_path.exists():
            # Try regenerating data if file missing
            verify_data_exists()
            if not viz_path.exists():
                return JSONResponse(
                    status_code=404,
                    content={
                        "error": "Visualization not found",
                        "detail": f"The requested visualization for {model}/{dimension}/{condition} was not found even after regeneration attempt.",
                        "path": str(viz_path),
                        "regeneration_attempted": True
                    }
                )
        
        try:
            return FileResponse(
                str(viz_path),
                media_type="image/png",
                filename=f"{condition}.png"
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Error serving visualization",
                    "detail": str(e),
                    "path": str(viz_path),
                    "media_type": "image/png",
                    "attempted_filename": f"{condition}.png"
                }
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Unexpected error",
                "detail": str(e)
            }
        )

if __name__ == "__main__":
    # Verify data exists before starting server
    verify_data_exists()
    
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
