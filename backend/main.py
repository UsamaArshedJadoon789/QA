from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Halal Compliance API"}

@app.get("/api/results")
async def get_results():
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

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
