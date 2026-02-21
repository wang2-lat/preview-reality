from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np

class ColorCalibrator:
    def create_comparison(self, input_path: str, output_path: str):
        img = Image.open(input_path).convert('RGB')
        
        # Create screen version (original)
        screen_version = img.copy()
        
        # Create print version (adjusted colors)
        print_version = self._simulate_print_colors(img)
        
        # Create side-by-side comparison
        width, height = img.size
        comparison = Image.new('RGB', (width * 2 + 40, height + 80), 'white')
        
        # Paste images
        comparison.paste(screen_version, (10, 60))
        comparison.paste(print_version, (width + 30, 60))
        
        # Add labels
        draw = ImageDraw.Draw(comparison)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((width // 2 - 50, 20), "Screen Display", fill='black', font=font)
        draw.text((width + width // 2 - 20, 20), "Print Result", fill='black', font=font)
        
        comparison.save(output_path)
    
    def _simulate_print_colors(self, img: Image.Image) -> Image.Image:
        # Simulate CMYK conversion effects
        img_array = np.array(img).astype(np.float32)
        
        # Reduce saturation (print is less vibrant)
        enhancer = ImageEnhance.Color(img)
        result = enhancer.enhance(0.85)
        
        # Slight darkening
        enhancer = ImageEnhance.Brightness(result)
        result = enhancer.enhance(0.95)
        
        # Reduce contrast slightly
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(0.92)
        
        return result
