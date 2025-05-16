import re
from difflib import SequenceMatcher

class LuminariaValidator:
    def __init__(self, reference_data):
        self.reference = reference_data  # Dados do PDF processado
    
    def validate_potency(self, extracted_value):
        # Padrões comuns de potência (ex: "50W", "100W LED")
        potency_pattern = r'(\d+)\s*W'
        match = re.search(potency_pattern, extracted_value)
        if not match:
            return None
        
        potency = float(match.group(1))
        
        # Verifica se está na faixa comum de potências
        if not (3 <= potency <= 500):  # Faixa razoável para luminárias
            return None
        
        # Compara com valores de referência
        closest = min(self.reference['potencies'], 
                     key=lambda x: abs(x - potency))
        
        if abs(closest - potency) < 5:  # Tolerância de 5W
            return closest
        return potency  # Retorna o valor extraído com warning
    
    def validate_model(self, extracted_model):
        # Comparação fuzzy com modelos conhecidos
        best_match = None
        best_ratio = 0
        
        for known_model in self.reference['models']:
            ratio = SequenceMatcher(None, extracted_model, known_model).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = known_model
        
        return best_match if best_ratio > 0.7 else extracted_model
    
    def cross_validate(self, extracted_data):
        validated = {}
        
        potency = self.validate_potency(extracted_data['text'])
        if potency:
            validated['potency'] = potency
        
        model = self.validate_model(extracted_data.get('model', ''))
        if model:
            validated['model'] = model
        
        # Validação adicional para LED baseada em múltiplos fatores
        is_led = extracted_data.get('is_led', False)
        if 'LED' in extracted_data['text'].upper():
            is_led = True
        validated['is_led'] = is_led
        
        return validated