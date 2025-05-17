import os
from dotenv import load_dotenv
from back_end.services.ai_service import AIService
from core.domain.entities import Luminaire

load_dotenv()

def main():
    # Configuração
    ai = AIService(os.getenv("TESSERACT_PATH"))
    
    # Exemplo de processamento
    sample_image = "assets/screenshots/SAAC-001.png"
    result = ai.process_image(sample_image)
    
    print(result.to_dict())

if __name__ == "__main__":
    main()