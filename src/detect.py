"""Carregamento e inferência do detector de EPI treinado localmente."""
from __future__ import annotations
from pathlib import Path
from time import perf_counter
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
CLASS_NAMES=('capacete','colete','oculos')

def model_path() -> Path:
    candidates=(ROOT/'models'/'best.pt',ROOT/'results'/'training'/'yolo11n_ppe3_fixed'/'weights'/'best.pt',ROOT.parent/'04_MODELO_TREINADO'/'best.pt')
    return next((candidate for candidate in candidates if candidate.is_file()), candidates[0])

def load_model():
    from ultralytics import YOLO
    path=model_path()
    if not path.is_file(): raise FileNotFoundError('Modelo treinado não encontrado. Execute training/train.py antes da inferência.')
    model=YOLO(str(path))
    if tuple(model.names.values()) != CLASS_NAMES: raise RuntimeError(f'Classes incompatíveis no peso: {model.names}')
    return model

def detect(image: np.ndarray, confidence: float=0.25, model=None):
    if not isinstance(image,np.ndarray) or image.size==0: raise ValueError('Imagem inválida ou vazia.')
    started=perf_counter(); model=model or load_model(); result=model.predict(source=image,conf=confidence,imgsz=416,device=0,verbose=False)[0]
    detections=[]
    for box in result.boxes:
        class_id=int(box.cls.item()); detections.append({'class_id':class_id,'class_name':CLASS_NAMES[class_id],
            'confidence':round(float(box.conf.item()),4),'xyxy':[round(float(value),1) for value in box.xyxy[0].tolist()]})
    return result.plot(),detections,round((perf_counter()-started)*1000,1)
