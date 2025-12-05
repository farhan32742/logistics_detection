from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from PIL import Image
import io
import os
import pathlib
import platform

# THE FIX: Handle the difference between Linux (Colab) and Windows paths
if platform.system() == 'Windows':
    pathlib.PosixPath = pathlib.WindowsPath

app = FastAPI()
model = YOLO("best.pt") 

@app.get("/")
def read_root():
    return {"message": "YOLO Object Detection API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validate input
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG/PNG allowed.")

    try:
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Run inference
        results = model(image)
        
        # Process results
        detections = []
        for result in results:
            # result.boxes contains the detection data
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist() # Bounding box coordinates
                confidence = box.conf[0].item()       # Confidence score
                class_id = int(box.cls[0].item())     # Class ID
                class_name = model.names[class_id]    # Class Name

                detections.append({
                    "box": [x1, y1, x2, y2],
                    "confidence": round(confidence, 2),
                    "class_id": class_id,
                    "class_name": class_name
                })

        return JSONResponse(content={"filename": file.filename, "detections": detections})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Main entry point for debugging locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)