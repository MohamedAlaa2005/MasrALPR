from collections import Counter


ARABIC_MAP = {
    '0':'٠', '1':'١', '2':'٢', '3':'٣', '4':'٤', 
    '5':'٥', '6':'٦', '7':'٧', '8':'٨', '9':'٩',
    'a':'أ', 'b':'ب', 'd':'د', 'r':'ر', 'sad':'ص', 
    'sen':'س', 't':'ط', 'en':'ع', 'f':'ف', 'q':'ق', 
    'k':'ك', 'l':'ل', 'mem':'م', 'non':'ن', 'h':'هـ', 
    'w':'و', 'y':'ي'
}

ARABIC_DIGITS = set('٠١٢٣٤٥٦٧٨٩0123456789')


def recognize_characters_improved(char_recognizer, plate_img):
    """
    Improved character recognition with better sorting and filtering
    """
    results = char_recognizer(plate_img)[0]
    detections = []
    
    for box in results.boxes:
        label = char_recognizer.names[int(box.cls[0])]
        confidence = box.conf[0].item()
        x_center = box.xywh[0][0].item()
        y_center = box.xywh[0][1].item()
        width = box.xywh[0][2].item()
        height = box.xywh[0][3].item()
        
        if confidence > 0.3:  # Lower threshold, filter later
            arabic_char = ARABIC_MAP.get(label, label)
            detections.append({
                'x': x_center,
                'y': y_center,
                'w': width,
                'h': height,
                'char': arabic_char,
                'confidence': confidence,
                'label': label
            })
    
    if not detections:
        return ""
    
    # IMPROVEMENT 1: Remove duplicate detections (same character, close position)
    detections = remove_duplicates(detections)
    
    # Sort left to right
    detections.sort(key=lambda d: d['x'])
    
    # Separate numbers and letters
    numbers = []
    letters = []
    
    for d in detections:
        if d['char'] in ARABIC_DIGITS:
            numbers.append(d['char'])
        else:
            letters.insert(0, d['char'])
    
    nums_str = "".join(numbers)
    lets_str = " ".join(letters)
    
    return f"{lets_str} {nums_str}".strip()


def remove_duplicates(detections, distance_threshold=20):
    """
    Remove duplicate detections that are too close to each other
    Keep the one with higher confidence
    """
    if len(detections) <= 1:
        return detections
    
    # Sort by confidence (highest first)
    sorted_dets = sorted(detections, key=lambda d: d['confidence'], reverse=True)
    
    kept = []
    for det in sorted_dets:
        is_duplicate = False
        for kept_det in kept:
            # Check if too close to existing detection
            dist = abs(det['x'] - kept_det['x'])
            if dist < distance_threshold:
                is_duplicate = True
                break
        
        if not is_duplicate:
            kept.append(det)
    
    return kept

def recognize_with_voting(char_recognizer, plate_images):
    """
    Run recognition on multiple versions and vote
    """
    all_results = []
    
    for img in plate_images:
        if img is not None and img.size > 0:
            text = recognize_characters_improved(char_recognizer, img)
            if text:
                all_results.append(text)
    
    if not all_results:
        return ""
    
    # Vote for most common result
    result_counts = Counter(all_results)
    best_result = result_counts.most_common(1)[0][0]
    
    return best_result