import os
from enum import Enum


DOWNLOAD_PATH =f"{os.getcwd()}\\Data\\raw"

MAIN_URL = "https://candidaturaspoderjudicial.ine.mx"
DETAILS_URL = lambda id: f"https://candidaturaspoderjudicial.ine.mx/detalleCandidato/{id}/11"
DYNAMIC_COLLAPSE_ID_SELECTOR = lambda index: f'panelHeader{index}'
DYNAMIC_COLLAPSE_CONTENT_CLASS_NAME = "div.ant-collapse-content.ant-collapse-content-active"
MODAL_CLOSE_CLASS = "ant-modal-close"

class CARGOS_NAME(Enum):
    SUPREMA_CORTE = 1
    TRIBUNAL_DISIPLINA = 2
    SALA_SUP_TRIBUNAL_ELE = 3
    SALA_REG_TRIBUNAL_ELE = 4
    MAGIS_CIRCUITO = 5
    JUECES_DISTRITO = 6