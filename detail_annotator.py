from PIL import Image, ImageDraw
import numpy as np

class DetailAnnotator:
    def annotate(self, input_path: str, output_path: str, threshold: float):
        img = Image.open(input_path).convert('RGB')
        img_array = np.array(img)
        
        # Detect high-frequency details (edges)
        gray = np.mean(img_array, axis=2)
        edges = self._detect_edges(gray)
        
        # Find areas with high detail density
        detail_areas = self._find_detail_areas(edges, threshold)
        
        # Annotate image
        result = img.copy()
        draw = ImageDraw.Draw(result, 'RGBA')
        
        for area in detail_areas:
            x, y, w, h = area
            # Draw semi-transparent red box
            draw.rectangle([x, y, x+w, y+h], outline=(255, 0, 0, 200), width=3)
            # Add warning label
            draw.rectangle([x, y-25, x+120, y], fill=(255, 0, 0, 180))
            draw.text((x+5, y-20), "Detail Risk", fill='white')
        
        result.save(output_path)
    
    def _detect_edges(self, gray: np.ndarray) -> np.ndarray:
        # Simple gradient-based edge detection
        h, w = gray.shape
        edges = np.zeros_like(gray)
        
        # Calculate gradients
        for y in range(1, h-1):
            for x in range(1, w-1):
                gx = abs(float(gray[y, x+1]) - float(gray[y, x-1]))
                gy = abs(float(gray[y+1, x]) - float(gray[y-1, x]))
                edges[y, x] = np.sqrt(gx**2 + gy**2)
        
        return edges
    
    def _find_detail_areas(self, edges: np.ndarray, threshold: float) -> list:
        # Find regions with high edge density
        h, w = edges.shape
        areas = []
        
        # Divide image into grid
        grid_size = 100
        max_edge = np.max(edges)
        
        for y in range(0, h - grid_size, grid_size // 2):
            for x in range(0, w - grid_size, grid_size // 2):
                region = edges[y:y+grid_size, x:x+grid_size]
                density = np.mean(region)
                
                # If density exceeds threshold, mark as detail area
                if density > threshold * max_edge:
                    areas.append((x, y, grid_size, grid_size))
        
        return areas
