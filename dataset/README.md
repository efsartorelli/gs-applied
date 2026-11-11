# Dataset Construction-PPE

Fonte: [Ultralytics Construction-PPE](https://docs.ultralytics.com/datasets/detect/construction-ppe), arquivo oficial de novembro de 2026. A fonte declara 1.000 imagens, 800 para treino e 200 para validação, com anotações YOLO e licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

O projeto não versiona imagens ou labels. Baixe e extraia o ZIP oficial em `dataset/source/construction-ppe`, depois execute:

```powershell
py -3.12 training/prepare_dataset.py
```

O script mantém somente os IDs originais `helmet=0`, `vest=2` e `goggles=4`, remapeados respectivamente para `capacete=0`, `colete=1` e `oculos=2`. Os 200 itens de validação originais são repartidos deterministicamente (seed 42) em 100 validação e 100 teste independente. A adaptação e a atribuição à Ultralytics devem ser mantidas em qualquer redistribuição.
