from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import matplotlib.pyplot as plt
import io
import os
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create results directory if it doesn't exist
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)
os.chmod(RESULTS_DIR, 0o777)

def generate_random_data():
    return {
        "slaughterhouse": {
            "condition1": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)},
            "condition2": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)},
            "condition3": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)},
            "condition4": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)},
            "condition5": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)},
            "condition6": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)}
        },
        "food_processing": {
            "condition1": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)},
            "condition2": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)},
            "condition3": {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)}
        }
    }

def generate_visualization(data, model_type, condition):
    plt.figure(figsize=(10, 6))
    condition_data = data[model_type][f"condition{condition}"]
    
    labels = ['Compliant', 'Non-Compliant']
    values = [condition_data['compliant'], condition_data['non_compliant']]
    
    plt.bar(labels, values, color=['green', 'red'])
    plt.title(f"{model_type.replace('_', ' ').title()} - Condition {condition}")
    plt.ylabel('Count')
    
    img_path = RESULTS_DIR / f"{model_type}_condition{condition}.png"
    plt.savefig(img_path)
    plt.close()
    
    return img_path

@app.get("/api/results")
async def get_results():
    try:
        data = generate_random_data()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/visualizations/{model_type}/2d/condition{condition}.png")
async def get_visualization(model_type: str, condition: int):
    try:
        data = generate_random_data()
        img_path = generate_visualization(data, model_type, condition)
        return FileResponse(img_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
