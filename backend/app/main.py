from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import matplotlib.pyplot as plt
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULTS_DIR = "/tmp/results"
os.makedirs(RESULTS_DIR, exist_ok=True)
os.chmod(RESULTS_DIR, 0o777)

def generate_test_data():
    data = {
        "slaughterhouse": {
            "conditions": {str(i): {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)} for i in range(1, 7)}
        },
        "food_processing": {
            "conditions": {str(i): {"compliant": np.random.randint(70, 100), "non_compliant": np.random.randint(0, 30)} for i in range(1, 4)}
        }
    }
    
    with open(os.path.join(RESULTS_DIR, "results.json"), "w") as f:
        json.dump(data, f)
    
    for model in ["slaughterhouse", "food_processing"]:
        conditions = data[model]["conditions"]
        for condition, values in conditions.items():
            plt.figure(figsize=(10, 6))
            plt.bar(["Compliant", "Non-Compliant"], [values["compliant"], values["non_compliant"]])
            plt.title(f"{model.title()} - Condition {condition}")
            plt.ylabel("Count")
            plt.savefig(os.path.join(RESULTS_DIR, f"{model}_condition{condition}.png"))
            plt.close()
    
    return data

@app.get("/")
async def root():
    return {"message": "Halal Compliance API is running"}

@app.get("/api/results")
async def get_results():
    try:
        data = generate_test_data()
        return data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/visualizations/{model}/2d/condition{condition}.png")
async def get_visualization(model: str, condition: int):
    from fastapi.responses import FileResponse
    file_path = os.path.join(RESULTS_DIR, f"{model}_condition{condition}.png")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Visualization not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
