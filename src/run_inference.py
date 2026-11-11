"""Executa inferência reproduzível sobre uma imagem e salva anotação + JSON."""
import argparse, json
from pathlib import Path
import cv2
from detect import detect

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--input',required=True); parser.add_argument('--output',default='results/predictions/example_test_annotated.jpg')
    args=parser.parse_args(); image=cv2.imread(args.input)
    if image is None: raise ValueError(f'Não foi possível ler a imagem: {args.input}')
    annotated,detections,elapsed=detect(image); output=Path(args.output); output.parent.mkdir(parents=True,exist_ok=True)
    if not cv2.imwrite(str(output),annotated): raise RuntimeError(f'Não foi possível gravar {output}')
    metadata=output.with_suffix('.json'); metadata.write_text(json.dumps({'input':args.input,'output':str(output),'detections':detections,'inference_ms':elapsed},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(output),'detections':len(detections),'inference_ms':elapsed},ensure_ascii=False))

if __name__=='__main__': main()
