"""Validação no holdout de teste, não empregado no treinamento nem na validação por época."""
import json
from pathlib import Path
from ultralytics import YOLO

ROOT=Path(__file__).resolve().parents[1]
WEIGHTS=ROOT/'results'/'training'/'yolo11n_ppe3_fixed'/'weights'/'best.pt'
DATA=ROOT/'dataset'/'ppe_3_classes_fixed'/'data.yaml'
OUT=ROOT/'results'/'metrics'

def main():
    if not WEIGHTS.is_file(): raise FileNotFoundError(f'Pesos ausentes: {WEIGHTS}')
    OUT.mkdir(parents=True,exist_ok=True)
    result=YOLO(str(WEIGHTS)).val(data=str(DATA),split='test',imgsz=416,batch=2,device=0,workers=0,plots=True,project=str(OUT),name='test_holdout',exist_ok=True)
    summary={'precision':float(result.box.mp),'recall':float(result.box.mr),'map50':float(result.box.map50),'map50_95':float(result.box.map),'per_class_map50_95':[float(v) for v in result.box.maps]}
    (OUT/'test_metrics.json').write_text(json.dumps(summary,indent=2),encoding='utf-8'); print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
