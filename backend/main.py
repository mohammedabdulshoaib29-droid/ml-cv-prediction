from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.dataset_routes import router as dataset_router
from routes.prediction_routes import router as prediction_router
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create datasets directory if it doesn't exist
os.makedirs("datasets", exist_ok=True)

app = FastAPI(
    title="ML-Based CV Behavior Prediction",
    description="Advanced machine learning for CV analysis and behavior forecasting",
    version="1.0.0"
)

# Add CORS middleware - simplified since frontend is now on same server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(dataset_router, prefix="/api", tags=["datasets"])
app.include_router(prediction_router, prefix="/api", tags=["predictions"])

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "ML API is running"}

# Serve static files from React build directory
# Check if frontend build exists
build_dir = Path(__file__).parent.parent / "frontend" / "build"

if build_dir.exists():
    app.mount("/", StaticFiles(directory=str(build_dir), html=True), name="static")
else:
    # Development fallback message
    @app.get("/")
    def root():
        return {
            "message": "ML-Based CV Behavior Prediction API",
            "api_docs": "/docs",
            "note": "Frontend not built. Run: cd frontend && npm install && npm run build"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
