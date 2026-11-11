# Treinamento customizado

Experimento válido: 11/11/2026, Windows, Python 3.12.10, PyTorch 2.7.1+cu118, Ultralytics 8.4.210, CUDA GPU NVIDIA RTX 3060. O log indicou aproximadamente 0,32 GB de VRAM alocada pelo treinamento.

| Parâmetro | Valor |
|---|---:|
| Arquitetura | YOLO11n pré-treinada, fine-tuning customizado |
| Épocas | 5 |
| Resolução | 416 px |
| Batch | 2 |
| Workers | 0 (Windows) |
| Seed | 42 |
| AMP | habilitado |
| Classes | capacete, colete, óculos |

Houve uma primeira tentativa inválida: o script gravou a sequência literal `\\n` nos labels, resultando em zero labels/métricas. O defeito foi identificado, corrigido com quebras de linha reais e o experimento `yolo11n_ppe3_fixed` foi reexecutado. Somente o segundo experimento é usado nos resultados.
