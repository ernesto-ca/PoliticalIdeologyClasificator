import os
from enum import Enum


DOWNLOAD_PATH =f"{os.getcwd()}\\Data\\raw"
PROCESSED_PATH =f"{os.getcwd()}\\Data\\processed"

class CARGOS_NAME(Enum):
    # numbers represent the id is used in the attribute from the html component
    SUPREMA_CORTE = 1
    TRIBUNAL_DISIPLINA = 3
    SALA_SUP_TRIBUNAL_ELE = 2
    SALA_REG_TRIBUNAL_ELE = 4
    MAGIS_CIRCUITO = 5
    JUECES_DISTRITO = 6

CARGOS_CONSULT_ID = {
    '1': 6,
    '3' : 7,
    '2': 8,
    '4' : 9,
    '5' : 10,
    '6' : 11
}

MAIN_URL = "https://candidaturaspoderjudicial.ine.mx"
DETAILS_URL = lambda id,cargo_id: f"https://candidaturaspoderjudicial.ine.mx/detalleCandidato/{id}/{CARGOS_CONSULT_ID[str(cargo_id)]}"
DYNAMIC_COLLAPSE_ID_SELECTOR = lambda index: f'panelHeader{index}'
DYNAMIC_COLLAPSE_CONTENT_CLASS_NAME = "div.ant-collapse-content.ant-collapse-content-active"
MODAL_CLOSE_CLASS = "ant-modal-close"

# Details Constants
DYNAMIC_CANDIDATE_CARDS = "div.ant-card.ant-card-bordered.cardSeccion"
FUNCTION_VISION_ID = 'titulo-vision-jurisdiccional'
IMPART_VISION_ID = 'titulo-vision-justicia'
PROPOSAL_CSS_ID = 'titulo-propuestas'

UNIONS_NAME = {
"poder ejecutivo": 1,
    "poder legislativo": 2,
    "poder judicial": 3,
    "en funciones": 4,
}
