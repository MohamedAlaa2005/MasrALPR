import os, uuid, cv2, numpy as np
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ultralytics import YOLO
from .database import SessionLocal, PlateRecord, BlacklistedPlate
from .image_enhancer import ImageEnhancer
from .multi_enhance import MultiEnhancer
from .recognition_improved import recognize_characters_improved, recognize_with_voting


app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Models
plate_detector = YOLO("app/weights/plate.pt")
char_recognizer = YOLO("app/weights/letter&number.pt")

# Enhancers
enhancer = ImageEnhancer()
multi_enhancer = MultiEnhancer()

# Post-processor


ARABIC_DIGITS = set('٠١٢٣٤٥٦٧٨٩0123456789')


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()


def detect_plate_location(img):
    results = plate_detector(img)[0]
    plates = []
    
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        confidence = box.conf[0].item()
        
        if confidence > 0.5:
            padding = 50
            h, w = img.shape[:2]
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(w, x2 + padding)
            y2 = min(h, y2 + padding)
            
            plate_crop = img[y1:y2, x1:x2]
            plates.append({
                'image': plate_crop,
                'bbox': (x1, y1, x2, y2),
                'confidence': confidence
            })
    
    return plates


def perform_ocr(img):
    """
    Improved OCR pipeline with multiple attempts and voting
    """
    # Step 1: Enhance full image
    enhanced_img = enhancer.enhance(img)
    
    # Step 2: Detect plates
    plates = detect_plate_location(enhanced_img)
    
    if not plates:
        return "Error 404"
    
    # Get best plate
    best_plate = max(plates, key=lambda p: p['confidence'])
    plate_crop = best_plate['image']
    
    # Step 3: Generate multiple enhanced versions of plate
    plate_versions = multi_enhancer.get_all_versions(plate_crop)
    
    # Step 4: Run recognition with voting
    plate_text = recognize_with_voting(char_recognizer, plate_versions)

    return plate_text



@app.post("/predict")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    
    plate_text = perform_ocr(img)
    
    if not plate_text:
        return {"plate": "", "allowed": True, "error": "No plate detected"}
    
    blacklist = db.query(BlacklistedPlate).all()
    is_allowed = not any(item.plate_text in plate_text for item in blacklist)

    img_name = f"{uuid.uuid4()}.jpg"
    
    db.add(PlateRecord(text=plate_text, is_allowed=is_allowed, image_name=img_name))
    db.commit()
    
    return {"plate": plate_text, "allowed": is_allowed}


@app.post("/predict-debug")
async def predict_debug(file: UploadFile = File(...)):
    """
    Debug endpoint that returns intermediate steps
    """
    contents = await file.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    
    # Step 1: Enhance
    enhanced_img = enhancer.enhance(img)
    
    # Step 2: Detect plates
    plates = detect_plate_location(enhanced_img)
    
    debug_info = {
        "original_size": img.shape[:2],
        "enhanced_size": enhanced_img.shape[:2],
        "plates_detected": len(plates),
        "plates": []
    }
    
    for i, plate in enumerate(plates):
        plate_crop = plate['image']
        enhanced_plate = enhancer.enhance_plate(plate_crop)
        plate_text = recognize_characters_improved(enhanced_plate)
        
        debug_info["plates"].append({
            "index": i,
            "bbox": plate['bbox'],
            "confidence": plate['confidence'],
            "crop_size": plate_crop.shape[:2],
            "enhanced_size": enhanced_plate.shape[:2],
            "text": plate_text
        })
    
    return debug_info


@app.post("/blacklist/add-by-photo")
async def add_bl_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    plate_text = perform_ocr(img)
    
    if not plate_text: 
        raise HTTPException(400, "No plate detected")
    
    if not db.query(BlacklistedPlate).filter_by(plate_text=plate_text).first():
        db.add(BlacklistedPlate(plate_text=plate_text))
        db.commit()
    
    return {"status": "success", "plate": plate_text}


@app.get("/blacklist")
def get_bl(db: Session = Depends(get_db)): 
    return db.query(BlacklistedPlate).all()


@app.post("/blacklist/add")
def add_bl(plate: str, db: Session = Depends(get_db)):
    db.add(BlacklistedPlate(plate_text=plate))
    db.commit()
    return {"status": "added"}


@app.delete("/blacklist/remove/{id}")
def rem_bl(id: int, db: Session = Depends(get_db)):
    db.query(BlacklistedPlate).filter_by(id=id).delete()
    db.commit()
    return {"status": "deleted"}


@app.get("/history")
def get_hist(db: Session = Depends(get_db)):
    return db.query(PlateRecord).order_by(PlateRecord.timestamp.desc()).limit(5).all()


@app.get("/")
def home(): 
    return FileResponse('frontend/index.html')