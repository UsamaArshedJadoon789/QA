from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
RESULTS_DIR = Path("/tmp/app/results")
VISUALIZATIONS_DIR = RESULTS_DIR / "visualizations"

def setup_directories():
    """Create and set permissions for required directories"""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(VISUALIZATIONS_DIR / "slaughterhouse" / "2d", exist_ok=True)
    os.makedirs(VISUALIZATIONS_DIR / "slaughterhouse" / "3d", exist_ok=True)
    os.makedirs(VISUALIZATIONS_DIR / "food_processing" / "2d", exist_ok=True)
    os.makedirs(VISUALIZATIONS_DIR / "food_processing" / "3d", exist_ok=True)
    
    # Set permissions
    os.chmod(str(RESULTS_DIR), 0o777)
    os.chmod(str(VISUALIZATIONS_DIR), 0o777)
    for root, dirs, files in os.walk(VISUALIZATIONS_DIR):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o777)

def generate_test_data():
    """Generate sample data and visualizations"""
    setup_directories()
    
    # Generate sample data
    slaughterhouse_data = {
        "total_animals": 1000,
        "compliant_events": 850,
        "non_compliant_events": 150,
        "processing_time": 120,
        "conditions": {
            "condition1": {"compliant": 800, "non_compliant": 200},
            "condition2": {"compliant": 850, "non_compliant": 150},
            "condition3": {"compliant": 900, "non_compliant": 100},
            "condition4": {"compliant": 950, "non_compliant": 50},
            "condition5": {"compliant": 875, "non_compliant": 125},
            "condition6": {"compliant": 825, "non_compliant": 175}
        }
    }
    
    food_processing_data = {
        "total_batches": 500,
        "compliant_batches": 450,
        "non_compliant_batches": 50,
        "processing_time": 90,
        "conditions": {
            "condition1": {"compliant": 450, "non_compliant": 50},
            "condition2": {"compliant": 475, "non_compliant": 25},
            "condition3": {"compliant": 460, "non_compliant": 40}
        }
    }
    
    # Save data
    with open(RESULTS_DIR / "slaughterhouse_results.json", "w") as f:
        json.dump(slaughterhouse_data, f)
    
    with open(RESULTS_DIR / "food_processing_results.json", "w") as f:
        json.dump(food_processing_data, f)
    
    # Generate visualizations
    for model, data in [("slaughterhouse", slaughterhouse_data), 
                       ("food_processing", food_processing_data)]:
        conditions = data["conditions"]
        for condition, values in conditions.items():
            # 2D visualization
            plt.figure(figsize=(10, 6))
            plt.bar(["Compliant", "Non-Compliant"], 
                   [values["compliant"], values["non_compliant"]])
            plt.title(f"{model.title()} - {condition} Compliance Results")
            plt.savefig(str(VISUALIZATIONS_DIR / model / "2d" / f"{condition}.png"))
            plt.close()
            
            # 3D visualization
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111, projection='3d')
            x = [0, 1]
            y = [0, 0]
            z = [values["compliant"], values["non_compliant"]]
            ax.bar3d(x, y, [0, 0], 0.5, 0.5, z)
            ax.set_title(f"{model.title()} - {condition} Compliance Results (3D)")
            ax.set_xticks([0.25, 1.25])
            ax.set_xticklabels(["Compliant", "Non-Compliant"])
            plt.savefig(str(VISUALIZATIONS_DIR / model / "3d" / f"{condition}.png"))
            plt.close()

@app.on_event("startup")
async def startup_event():
    """Generate test data on startup"""
    generate_test_data()

@app.get("/")
async def root():
    return {"message": "Halal Compliance API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/results")
async def get_results():
    """Get all simulation results"""
    try:
        slaughterhouse_file = RESULTS_DIR / "slaughterhouse_results.json"
        food_processing_file = RESULTS_DIR / "food_processing_results.json"
        
        results = {
            "slaughterhouse": json.loads(slaughterhouse_file.read_text()) if slaughterhouse_file.exists() else {},
            "food_processing": json.loads(food_processing_file.read_text()) if food_processing_file.exists() else {}
        }
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/visualizations/{model}/{dimension}/{condition}")
async def get_visualization(model: str, dimension: str, condition: str):
    """Get visualization image"""
    try:
        file_path = VISUALIZATIONS_DIR / model / dimension / f"{condition}.png"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Visualization not found")
        return FileResponse(str(file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
