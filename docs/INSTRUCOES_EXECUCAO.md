# Instruções de execução e reprodução

## Pré-requisitos

Windows 10/11, Python 3.12 e, para reproduzir a aceleração original, uma instalação CUDA compatível com PyTorch. O projeto também pode executar em CPU se `device` for alterado para `cpu` em `training/training_config.yaml`.

## Executar a demonstração

```powershell
py -3.12 -m venv .venv-cv
.\.venv-cv\Scripts\Activate.ps1
pip install torch==2.7.1 torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
streamlit run src/app.py
```

No pacote de entrega, execute os comandos dentro de `03_CODIGO_FONTE`. O resolvedor de modelo procura automaticamente `../04_MODELO_TREINADO/best.pt`. Abra `http://localhost:8501` e envie `examples/demo_input.jpg` ou outra imagem autorizada.

## Verificar

```powershell
python -m unittest discover -s tests -v
python src/run_inference.py --input examples/demo_input.jpg
```

## Reproduzir dados, treinamento e validação

Baixe o Construction-PPE oficial, licenciado em CC BY 4.0, extraia-o em `dataset/source/construction-ppe` e execute:

```powershell
python training/prepare_dataset.py
python training/train.py
python training/validate.py
```

O dataset completo não acompanha a entrega por seu tamanho. A preparação conserva helmet, vest e goggles, remapeados para capacete, colete e oculos. O modelo distribuído é o peso real validado no experimento de cinco épocas; métricas e limites estão em `docs/RESULTADOS.md`.
