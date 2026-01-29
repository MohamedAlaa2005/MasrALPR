import os, uuid, cv2, numpy as np
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ultralytics import YOLO
from .database import SessionLocal, PlateRecord, BlacklistedPlate

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

model = YOLO("app/weights/best.pt")

ARABIC_MAP = {
    '1':'١', '2':'٢', '3':'٣', '4':'٤', '5':'٥', '6':'٦', '7':'٧', '8':'٨', '9':'٩',
    'a':'أ', 'b':'ب', 'd':'د', 'r':'ر', 'sad':'ص', 'sen':'س', 't':'ط', 'en':'ع', 
    'f':'ف', 'q':'ق', 'k':'ك', 'l':'ل', 'mem':'م', 'non':'ن', 'h':'هـ', 'w':'و', 'y':'ي'
}

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()


def perform_ocr(img):
    results = model(img)[0]
    detections = []
    for box in results.boxes:
        label = model.names[int(box.cls[0])]
        if label != 'car plate':
            # Store the x-coordinate and the Arabic character
            detections.append((box.xywh[0][0].item(), ARABIC_MAP.get(label, label)))
    
    # Sort detections from left to right based on x-coordinate
    detections.sort(key=lambda x: x[0])
    # Separate numbers and letters dynamically
    nums_list = [d[1] for d in detections if d[1].isdigit() or d[1] in '٠١٢٣٤٥٦٧٨٩']
    detections.sort(key=lambda x: x[1])
    lets_list = [d[1] for d in detections if d[1] not in nums_list]

    # Join them with a clear separation
    nums = "".join(nums_list)
    lets = " ".join(lets_list)
    
    # Return formatted text
    return f"{lets} {nums}"

@app.post("/predict")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    plate_text = perform_ocr(img)
    
    blacklist = db.query(BlacklistedPlate).all()
    is_allowed = not any(item.plate_text in plate_text for item in blacklist)

    img_name = f"{uuid.uuid4()}.jpg"
    cv2.imwrite(f"static/captures/{img_name}", img)
    db.add(PlateRecord(text=plate_text, is_allowed=is_allowed, image_name=img_name))
    db.commit()
    return {"plate": plate_text, "allowed": is_allowed}

@app.post("/blacklist/add-by-photo")
async def add_bl_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    plate_text = perform_ocr(img)
    if not plate_text: raise HTTPException(400, "No plate detected")
    
    if not db.query(BlacklistedPlate).filter_by(plate_text=plate_text).first():
        db.add(BlacklistedPlate(plate_text=plate_text))
        db.commit()
    return {"status": "success", "plate": plate_text}

@app.get("/blacklist")
def get_bl(db: Session = Depends(get_db)): return db.query(BlacklistedPlate).all()

@app.post("/blacklist/add")
def add_bl(plate: str, db: Session = Depends(get_db)):
    db.add(BlacklistedPlate(plate_text=plate)); db.commit()
    return {"status": "added"}

@app.delete("/blacklist/remove/{id}")
def rem_bl(id: int, db: Session = Depends(get_db)):
    db.query(BlacklistedPlate).filter_by(id=id).delete()
    db.commit(); return {"status": "deleted"}

@app.get("/history")
def get_hist(db: Session = Depends(get_db)):
    return db.query(PlateRecord).order_by(PlateRecord.timestamp.desc()).limit(5).all()


@app.get("/")
def home(): return FileResponse('frontend/index.html')