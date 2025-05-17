from dataclasses import dataclass
from enum import Enum

class LuminaireStatus(Enum):
    SUCCESS = "SUCESSO"
    ERROR = "ERRO"

@dataclass
class Luminaire:
    saac_id: str
    potencia: float
    tipo: str
    modelo: str
    status: LuminaireStatus
    
    def to_dict(self):
        return {
            "ID_SAAC": self.saac_id,
            "POTENCIA": self.potencia,
            "TIPO": self.tipo,
            "MODELO": self.modelo,
            "STATUS": self.status.value
        }