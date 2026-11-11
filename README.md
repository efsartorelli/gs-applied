# Quem Faz — Applied Computer Vision

MVP acadêmico da Global Solution FIAP 2026.2 para detecção de equipamentos de proteção individual (EPIs) em imagens. O sistema usa um modelo YOLO11n treinado localmente para reconhecer **capacete**, **colete** e **óculos de proteção**. É uma demonstração de apoio à inspeção visual: não certifica conformidade nem substitui procedimentos de segurança, avaliação humana ou normas regulamentadoras.

## Integrantes

- Enzo Vazquez Sartorelli — RM 94618
- Kaue Pastori Teixeira — RM 98501
- Nicolas Nogueira Boni — RM 551965
- Guilherme Brazioli — RM 98237
- Pedro Oliveira Valotto — RM 551445

Relação acadêmica padronizada em [docs/AUTORES.md](docs/AUTORES.md).

## Resultado reproduzível

No teste holdout de 100 imagens, separado deterministicamente antes do treinamento, o modelo obteve precisão 0,8892, recall 0,7177, mAP@50 0,7691 e mAP@50-95 0,4991. As métricas, limitações e evidências estão em [docs/RESULTADOS.md](docs/RESULTADOS.md). O peso efetivamente validado está em `models/best.pt`.

## Demonstração gravada

A demonstração automatizada usa uploads reais na interface Streamlit e executa inferências de capacete, colete, óculos e múltiplos objetos. O arquivo final está em [entrega/VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4](entrega/VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4); veja os detalhes e a validação em [entrega/RELATORIO_GRAVACAO.md](entrega/RELATORIO_GRAVACAO.md) e [entrega/VALIDACAO_VIDEO.json](entrega/VALIDACAO_VIDEO.json).

## Execução local

Requer Python 3.12+ e, para a configuração acelerada utilizada, CUDA compatível com PyTorch.

```powershell
py -3.12 -m venv .venv-cv
.\.venv-cv\Scripts\Activate.ps1
pip install torch==2.7.1 torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
streamlit run src/app.py
```

Abra `http://localhost:8501`, envie uma imagem e selecione o limiar de confiança. Para inferência por linha de comando:

```powershell
python src/run_inference.py --input caminho\para\imagem.jpg
```

O comando PyTorch acima reproduz o ambiente CUDA 11.8 usado no experimento. Confirme a combinação apropriada para seu driver na documentação oficial do PyTorch antes de treinar; para CPU, altere `device` em `training/training_config.yaml` e espere execução significativamente mais lenta.

Para vídeo local:

```powershell
python src/process_video.py --input caminho\para\video.mp4
```

## Treinamento e dados

O conjunto original é o Construction-PPE da Ultralytics, sob CC BY 4.0. O repositório não inclui imagens ou rótulos do dataset. Baixe o arquivo original, extraia em `dataset/source/construction-ppe` e execute:

```powershell
python training/prepare_dataset.py
python training/train.py
python training/validate.py
```

O script reduz e remapeia as classes originais `helmet`, `vest` e `goggles` para `capacete`, `colete` e `oculos`, usando seed 42. Consulte [dataset/README.md](dataset/README.md) e [docs/TREINAMENTO.md](docs/TREINAMENTO.md) para atribuição, licença, partição e hiperparâmetros.

## Estrutura

```text
src/        interface Streamlit e inferência
training/   preparação, treinamento e validação
models/     peso final validado
results/    métricas, gráficos e exemplos curados
tests/      testes automatizados
docs/       arquitetura, método, resultados e conformidade
entrega/    relatório PDF e materiais para vídeo
```

## Verificação

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src training tests
```

## Licenças e atribuição

O código deste repositório está sob MIT ([LICENSE](LICENSE)). O dataset não é redistribuído aqui e permanece sob CC BY 4.0, com atribuição à Ultralytics. O uso do software Ultralytics/YOLO está sujeito à licença aplicável do respectivo projeto. Veja [dataset/README.md](dataset/README.md).
