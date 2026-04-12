from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import os

router = APIRouter()

# Get datasets directory - works in both local and Render
BACKEND_DIR = Path(__file__).parent.parent
DATASETS_DIR = BACKEND_DIR / "datasets"

# Ensure datasets directory exists
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.csv'}

@router.get("/datasets")
async def get_datasets():
    """Get list of all available datasets"""
    try:
        if not DATASETS_DIR.exists():
            DATASETS_DIR.mkdir(parents=True, exist_ok=True)
            return {"datasets": []}
        
        datasets = []
        for file in DATASETS_DIR.iterdir():
            if file.suffix in ALLOWED_EXTENSIONS:
                datasets.append({
                    "name": file.name,
                    "size": file.stat().st_size,
                    "type": file.suffix
                })
        
        return {"datasets": sorted(datasets, key=lambda x: x['name'])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading datasets: {str(e)}")

@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload and save a new dataset"""
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Create datasets directory if it doesn't exist
        DATASETS_DIR.mkdir(exist_ok=True)
        
        # Save file
        file_path = DATASETS_DIR / file.filename
        
        # Handle duplicate filenames
        if file_path.exists():
            # Append timestamp or version number
            import time
            name, ext = Path(file.filename).stem, file_ext
            file_path = DATASETS_DIR / f"{name}_{int(time.time())}{ext}"
        
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        return {
            "message": "Dataset uploaded successfully",
            "filename": file_path.name,
            "size": len(content)
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.delete("/datasets/{dataset_name}")
async def delete_dataset(dataset_name: str):
    """Delete a dataset"""
    try:
        file_path = DATASETS_DIR / dataset_name
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        file_path.unlink()
        
        return {"message": f"Dataset {dataset_name} deleted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting dataset: {str(e)}")
