"""Treinamento customizado, conservador para 4 GB de VRAM no Windows."""
import json
from pathlib import Path
from ultralytics import YOLO

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'dataset'/'ppe_3_classes_fixed'/'data.yaml'
OUT=ROOT/'results'/'training'
CONFIG={'model':'yolo11n.pt','epochs':5,'imgsz':416,'batch':2,'workers':0,'device':0,'seed':42,'patience':5,'amp':True}

def main():
    if not DATA.is_file(): raise FileNotFoundError(f'Prepare o dataset antes: {DATA}')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'experiment_config.json').write_text(json.dumps(CONFIG,indent=2),encoding='utf-8')
    model=YOLO(CONFIG['model'])
    model.train(data=str(DATA),project=str(OUT),name='yolo11n_ppe3_fixed',exist_ok=True,**{k:v for k,v in CONFIG.items() if k!='model'})

if __name__=='__main__': main()
