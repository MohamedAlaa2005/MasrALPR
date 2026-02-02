import cv2
import numpy as np


class ImageEnhancer:
    """
    Improved image enhancement for license plate recognition
    """
    
    def __init__(self, scale_factor=2):
        self.scale_factor = scale_factor
    
    def enhance(self, img):
        """
        Enhanced preprocessing pipeline
        """
        if img is None:
            return img
        
        # Step 1: Denoise
        denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        
        # Step 2: Upscale
        h, w = denoised.shape[:2]
        upscaled = cv2.resize(
            denoised, 
            (w * self.scale_factor, h * self.scale_factor), 
            interpolation=cv2.INTER_CUBIC
        )
        
        # Step 3: CLAHE contrast enhancement
        lab = cv2.cvtColor(upscaled, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Step 4: Sharpen
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        
        # Blend for natural look
        result = cv2.addWeighted(enhanced, 0.7, sharpened, 0.3, 0)
        
        return result
    
    def enhance_plate_aggressive(self, img):
        """
        More aggressive enhancement specifically for plate crops
        """
        if img is None:
            return img
        
        # Step 1: Denoise more aggressively
        denoised = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 7, 21)
        
        # Step 2: Upscale more for small plates
        h, w = denoised.shape[:2]
        min_height = 150
        if h < min_height:
            scale = min_height / h
        else:
            scale = self.scale_factor
        
        upscaled = cv2.resize(
            denoised, 
            (int(w * scale), int(h * scale)), 
            interpolation=cv2.INTER_CUBIC
        )
        
        # Step 3: Stronger CLAHE
        lab = cv2.cvtColor(upscaled, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Step 4: Unsharp masking (better than simple sharpen)
        gaussian = cv2.GaussianBlur(enhanced, (0, 0), 3)
        sharpened = cv2.addWeighted(enhanced, 1.5, gaussian, -0.5, 0)
        
        return sharpened