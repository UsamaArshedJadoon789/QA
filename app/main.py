from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, Response
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

# Data directory for simulation results
RESULTS_DIR = Path("results")
VISUALIZATIONS_DIR = RESULTS_DIR / "visualizations"

# Call verify_data_exists during startup
@app.on_event("startup")
async def startup_event():
    """Initialize the application and generate test data."""
    print("Starting application initialization...")
    try:
        # Create results directory if it doesn't exist
        os.makedirs('app/results', exist_ok=True)
        os.makedirs('app/results/visualizations', exist_ok=True)
        
        # Set permissions
        os.chmod('app/results', 0o777)
        os.chmod('app/results/visualizations', 0o777)
        
        # Generate test data
        verify_data_exists()
        print("Application initialization completed successfully")
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        raise

def verify_data_exists():
    """Verify that all required data files and directories exist."""
    print(f"Starting data verification process with enhanced logging...")
    
    # Check Python environment and dependencies
    try:
        import matplotlib
        print(f"Matplotlib backend: {matplotlib.get_backend()}")
        print(f"Matplotlib configuration: {matplotlib.rcParams['backend']}")
    except Exception as e:
        print(f"Error checking matplotlib: {str(e)}")
    
    # Create and set permissions for results directory
    try:
        os.makedirs('results', exist_ok=True)
        os.chmod('results', 0o777)
        print(f"Results directory created and permissions set: {oct(os.stat('results').st_mode)[-3:]}")
    except Exception as e:
        print(f"Error creating results directory: {str(e)}")
    
    # Create visualization directories with detailed logging
    models = ['slaughterhouse', 'food_processing']
    dimensions = ['2d', '3d']
    for model in models:
        for dim in dimensions:
            try:
                viz_dir = VISUALIZATIONS_DIR / model / dim
                viz_dir.mkdir(parents=True, exist_ok=True)
                os.chmod(str(viz_dir), 0o777)
                print(f"Created visualization directory: {viz_dir}")
                print(f"Directory permissions: {oct(os.stat(str(viz_dir)).st_mode)[-3:]}")
                print(f"Directory exists: {viz_dir.exists()}")
            except Exception as e:
                print(f"Error creating visualization directory {viz_dir}: {str(e)}")
    
    required_files = [
        RESULTS_DIR / "slaughterhouse_results.json",
        RESULTS_DIR / "food_processing_results.json"
    ]
    
    # Always regenerate visualizations on startup
    print(f"Forcing regeneration of data and visualizations...")
    print(f"Current directory contents: {os.listdir(str(RESULTS_DIR))}")
    # Clear any existing visualizations
    import shutil
    for model in ['slaughterhouse', 'food_processing']:
        for dim in ['2d', '3d']:
            viz_dir = VISUALIZATIONS_DIR / model / dim
            if viz_dir.exists():
                shutil.rmtree(str(viz_dir))
            viz_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(str(viz_dir), 0o777)
        
        try:
            env = os.environ.copy()
            env['PYTHONPATH'] = str(Path(__file__).parent)
            env['MPLBACKEND'] = 'Agg'  # Force Agg backend
            
            print(f"Running generate_test_data.py with PYTHONPATH={env['PYTHONPATH']}")
            result = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "generate_test_data.py")],
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            print(f"Data generation stdout: {result.stdout}")
            print(f"Data generation stderr: {result.stderr}")
            print("Data and visualization generation completed")
            
            # Verify visualization files were created
            for model in models: 
                for dim in dimensions:
                    viz_path = VISUALIZATIONS_DIR / model / dim
                    try:
                        files = list(viz_path.glob('*.png'))
                        print(f"Generated visualizations for {model}/{dim}: {len(files)} files")
                        print(f"Files: {[f.name for f in files]}")
                    except Exception as e:
                        print(f"Error checking visualization files in {viz_path}: {str(e)}")
        except subprocess.CalledProcessError as e:
            print(f"Error running generate_test_data.py: {str(e)}")
            print(f"Process stdout: {e.stdout}")
            print(f"Process stderr: {e.stderr}")
            raise RuntimeError(f"Failed to generate required data files: {str(e)}")
        except Exception as e:
            print(f"Unexpected error during data generation: {str(e)}")
            raise
        # Verify all directories exist after generation
        for model in models:
            for dim in dimensions:
                viz_dir = VISUALIZATIONS_DIR / model / dim
                if not viz_dir.exists():
                    print(f"Warning: Directory {viz_dir} still does not exist after generation")
                else:
                    print(f"Success: Directory {viz_dir} exists with contents: {list(viz_dir.glob('*.png'))}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist with proper permissions
RESULTS_DIR.mkdir(exist_ok=True)
os.chmod(str(RESULTS_DIR), 0o777)
VISUALIZATIONS_DIR.mkdir(exist_ok=True, parents=True)
os.chmod(str(VISUALIZATIONS_DIR), 0o777)

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
        # Enhanced logging at start of request
        print(f"\n=== Visualization Request ===")
        print(f"Model: {model}, Dimension: {dimension}, Condition: {condition}")
        
        # Remove .png from condition if it's already there
        condition = condition.replace('.png', '')
        # Add 'condition' prefix if not present
        if not condition.startswith('condition'):
            condition = f"condition{condition}"
            
        viz_path = VISUALIZATIONS_DIR / model / dimension / f"{condition}.png"
        print(f"\nVisualization Path Details:")
        print(f"Full path: {viz_path}")
        print(f"Working directory: {os.getcwd()}")
        print(f"RESULTS_DIR exists: {os.path.exists(RESULTS_DIR)}")
        print(f"VISUALIZATIONS_DIR exists: {os.path.exists(VISUALIZATIONS_DIR)}")
        
        # Check directory structure
        model_dir = VISUALIZATIONS_DIR / model
        dim_dir = model_dir / dimension
        print(f"\nDirectory Structure:")
        print(f"Model dir ({model_dir}) exists: {os.path.exists(model_dir)}")
        print(f"Dimension dir ({dim_dir}) exists: {os.path.exists(dim_dir)}")
        
        # Set proper headers for static file serving
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': '*',
            'Cache-Control': 'no-cache'
        }
        
        if os.path.exists(dim_dir):
            print(f"\nContents of {dim_dir}:")
            print(os.listdir(dim_dir))
            
        # Check file existence and permissions
        if os.path.exists(viz_path):
            print(f"\nFile Details:")
            print(f"File exists: True")
            print(f"File permissions: {oct(os.stat(viz_path).st_mode)[-3:]}")
            print(f"File size: {os.path.getsize(viz_path)} bytes")
        
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
            if not viz_path.exists():
                # Try regenerating data if file missing
                verify_data_exists()
            
            if viz_path.exists():
                with open(str(viz_path), 'rb') as f:
                    image_bytes = f.read()
                
                headers.update({
                    'Content-Type': 'image/png',
                    'Content-Disposition': f'inline; filename="{condition}.png"'
                })
                
                return Response(
                    content=image_bytes,
                    media_type="image/png",
                    headers=headers
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
