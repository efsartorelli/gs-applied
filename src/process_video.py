"""Processa um vídeo autorizado, gravando um MP4 anotado sem persistir dados externos."""
import argparse
from pathlib import Path
import cv2
from detect import load_model

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--input',required=True); parser.add_argument('--output',default='results/predictions/video_annotated.mp4')
    args=parser.parse_args(); source=Path(args.input); output=Path(args.output); output.parent.mkdir(parents=True,exist_ok=True)
    if not source.is_file(): raise FileNotFoundError(source)
    capture=cv2.VideoCapture(str(source)); width=int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)); height=int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)); fps=capture.get(cv2.CAP_PROP_FPS) or 24
    writer=cv2.VideoWriter(str(output),cv2.VideoWriter_fourcc(*'mp4v'),fps,(width,height)); model=load_model()
    while True:
        ok,frame=capture.read()
        if not ok: break
        writer.write(model.predict(frame,conf=0.25,imgsz=416,device=0,verbose=False)[0].plot())
    capture.release(); writer.release(); print(output)
if __name__=='__main__': main()
