from enum import Enum

class EnumClassification(str, Enum):
    viniferas = "Viníferas"
    americanas_e_hibridas = "Americanas e híbridas"
    uvas_de_mesa = "Uvas de mesa"
    sem_classificacao = "Sem classificação"
