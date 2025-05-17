import cv2
import pytesseract
from core.domain.entities import Luminaire

class AIService:
    def __init__(self, tesseract_path: str):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def process_image(self, image_path: str) -> Luminaire:
        try:
            # 1. Pré-processamento
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 2. Extração de texto
            text = pytesseract.image_to_string(gray)
            
            # 3. Análise (simplificada)
            data = self._parse_text(text)
            
            return Luminaire(
                saac_id=data.get("id"),
                potencia=data.get("potencia", 0),
                tipo=data.get("tipo", "DESCONHECIDO"),
                modelo=data.get("modelo", "INDEFINIDO"),
                status=LuminaireStatus.SUCCESS
            )
        except Exception as e:
            return Luminaire(
                saac_id=image_path.stem,
                potencia=0,
                tipo="ERRO",
                modelo=str(e),
                status=LuminaireStatus.ERROR
            )
            