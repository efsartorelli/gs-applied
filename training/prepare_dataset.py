"""Cria o subconjunto reproduzível capacete/colete/óculos a partir do Construction-PPE."""
import argparse, json, random, shutil
from collections import Counter
from pathlib import Path

SOURCE_TO_TARGET={0:0,2:1,4:2}
TARGET_NAMES=['capacete','colete','oculos']

def remap_label(source, target):
    rows=[]
    if source.exists():
        for line in source.read_text(encoding='utf-8').splitlines():
            parts=line.split()
            if len(parts)==5 and int(parts[0]) in SOURCE_TO_TARGET:
                rows.append(' '.join([str(SOURCE_TO_TARGET[int(parts[0])])]+parts[1:]))
    target.write_text(chr(10).join(rows)+(chr(10) if rows else ''),encoding='utf-8')
    return Counter(int(row.split()[0]) for row in rows)

def copy_split(source_root, destination_root, split, names):
    counts=Counter()
    for image in names:
        source_split='train' if split=='train' else 'val'
        rel=image.relative_to(source_root/'images'/source_split)
        label=source_root/'labels'/source_split/rel.with_suffix('.txt')
        image_dest=destination_root/'images'/split/rel
        label_dest=destination_root/'labels'/split/rel.with_suffix('.txt')
        image_dest.parent.mkdir(parents=True,exist_ok=True); label_dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(image,image_dest); counts.update(remap_label(label,label_dest))
    return counts

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,default=Path('dataset/source/construction-ppe'))
    parser.add_argument('--output',type=Path,default=Path('dataset/ppe_3_classes'))
    args=parser.parse_args(); source=args.source.resolve(); output=args.output.resolve()
    if not (source/'data.yaml').is_file(): raise FileNotFoundError(f'Dataset fonte ausente: {source}')
    if output.exists() and any(output.iterdir()): raise FileExistsError(f'Saída já existe: {output}; remova-a manualmente apenas se desejar recriar.')
    train=sorted((source/'images/train').glob('*.*'))
    holdout=sorted((source/'images/val').glob('*.*'))
    rng=random.Random(42); rng.shuffle(holdout); val,test=holdout[:100],holdout[100:]
    report={'source':str(source),'seed':42,'mapping':{'helmet':'capacete','vest':'colete','goggles':'oculos'},'splits':{}}
    for split,images in [('train',train),('val',val),('test',test)]:
        counts=copy_split(source,output,split,images)
        report['splits'][split]={'images':len(images),'instances':{TARGET_NAMES[key]:counts[key] for key in range(3)}}
    (output/'data.yaml').write_text('path: '+output.as_posix()+'\ntrain: images/train\nval: images/val\ntest: images/test\nnames:\n  0: capacete\n  1: colete\n  2: oculos\n',encoding='utf-8')
    (output/'dataset_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
