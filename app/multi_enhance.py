import cv2
import numpy as np


class MultiEnhancer:
    """
    Try multiple enhancement methods and use best result
    """
    
    def __init__(self, scale_factor=2):
        self.scale_factor = scale_factor
    
    def get_all_versions(self, img):
        """
        Generate multiple preprocessed versions
        """
        versions = []
        
        # Version 1: Standard enhancement
        versions.append(self._standard_enhance(img))
        
        # Version 2: High contrast
        versions.append(self._high_contrast(img))
        
        # Version 3: Brightness adjusted (for dark images)
        versions.append(self._brighten(img))
        
        # Version 4: Brightness reduced (for overexposed)
        versions.append(self._darken(img))
        
        return versions
    
    def _standard_enhance(self, img):
        denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        h, w = denoised.shape[:2]
        upscaled = cv2.resize(denoised, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
        
        lab = cv2.cvtColor(upscaled, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    
    def _high_contrast(self, img):
        enhanced = self._standard_enhance(img)
        
        # Increase contrast
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Stretch histogram
        l = cv2.normalize(l, None, 0, 255, cv2.NORM_MINMAX)
        
        result = cv2.merge([l, a, b])
        return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    
    def _brighten(self, img):
        enhanced = self._standard_enhance(img)
        
        # Increase brightness
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, 30)
        v = np.clip(v, 0, 255).astype(np.uint8)
        
        result = cv2.merge([h, s, v])
        return cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
    
    def _darken(self, img):
        enhanced = self._standard_enhance(img)
        
        # Decrease brightness
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.subtract(v, 30)
        v = np.clip(v, 0, 255).astype(np.uint8)
        
        result = cv2.merge([h, s, v])
        return cv2.cvtColor(result, cv2.COLOR_HSV2BGR)