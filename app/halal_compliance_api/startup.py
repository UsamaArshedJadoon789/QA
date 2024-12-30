import os
import sys
import os
from generate_test_data import generate_test_data
import uvicorn

def main():
    # Ensure we have proper permissions
    os.umask(0)
    
    # Generate test data first
    print("Generating test data...")
    generate_test_data()
    
    # Start the server
    print("Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

if __name__ == "__main__":
    main()
