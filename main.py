from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import os

app = FastAPI()

# Enable CORS so React can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
model_path = "best.pt"
if not os.path.exists(model_path):
    print(f"Warning: {model_path} not found. Ensure it is uploaded.")
else:
    model = YOLO(model_path) 

@app.get("/")
def read_root():
    return {"message": "YOLO API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validate Image Type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Use JPEG or PNG.")

    try:
        # Read the file sent from React
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Run Inference
        # imgsz=640: Matches the Resize we do in React
        # conf=0.25: Only show detections with >25% confidence
        results = model(image, imgsz=640, conf=0.25)
        
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist() 
                confidence = box.conf[0].item()       
                class_id = int(box.cls[0].item())     
                class_name = model.names[class_id]    

                detections.append({
                    "box": [x1, y1, x2, y2],
                    "confidence": round(confidence, 2),
                    "class_id": class_id,
                    "class_name": class_name
                })

        return JSONResponse(content={
            "filename": file.filename, 
            "detections": detections
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)