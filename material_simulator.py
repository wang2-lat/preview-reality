from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

class MaterialSimulator:
    def apply_material(self, input_path: str, output_path: str, material: str):
        img = Image.open(input_path).convert('RGB')
        
        if material == "canvas":
            result = self._apply_canvas(img)
        elif material == "paper":
            result = self._apply_paper(img)
        elif material == "fabric":
            result = self._apply_fabric(img)
        else:
            result = img
        
        result.save(output_path)
    
    def _apply_canvas(self, img: Image.Image) -> Image.Image:
        # Add canvas texture
        img_array = np.array(img)
        noise = np.random.randint(-8, 8, img_array.shape, dtype=np.int16)
        textured = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        result = Image.fromarray(textured)
        
        # Slight blur for canvas weave
        result = result.filter(ImageFilter.GaussianBlur(0.5))
        
        # Reduce saturation slightly
        enhancer = ImageEnhance.Color(result)
        result = enhancer.enhance(0.9)
        
        return result
    
    def _apply_paper(self, img: Image.Image) -> Image.Image:
        # Paper texture with slight yellowing
        img_array = np.array(img)
        
        # Add fine grain
        noise = np.random.randint(-5, 5, img_array.shape, dtype=np.int16)
        textured = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        result = Image.fromarray(textured)
        
        # Slight warm tone
        enhancer = ImageEnhance.Color(result)
        result = enhancer.enhance(0.95)
        
        return result
    
    def _apply_fabric(self, img: Image.Image) -> Image.Image:
        # Fabric texture with more pronounced weave
        img_array = np.array(img)
        
        # Stronger texture
        noise = np.random.randint(-12, 12, img_array.shape, dtype=np.int16)
        textured = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        result = Image.fromarray(textured)
        
        # More blur for fabric softness
        result = result.filter(ImageFilter.GaussianBlur(1.0))
        
        # Reduce brightness slightly
        enhancer = ImageEnhance.Brightness(result)
        result = enhancer.enhance(0.95)
        
        return result
