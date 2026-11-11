# Resultados experimentais reais

Avaliação no teste independente de 100 imagens e 390 instâncias, nunca usado nas cinco épocas:

| Métrica | Resultado |
|---|---:|
| Precision | 0,889 |
| Recall | 0,718 |
| mAP@50 | 0,769 |
| mAP@50:95 | 0,499 |

| Classe | Instâncias no teste | mAP@50:95 |
|---|---:|---:|
| Capacete | 146 | 0,476 |
| Colete | 170 | 0,614 |
| Óculos | 74 | 0,407 |

Os arquivos de origem da avaliação incluem curvas Precision–Recall, F1, matriz de confusão e exemplos anotados em `results/metrics/test_holdout/`; cópias curadas estão em `results/plots/` e `results/predictions/`. A inferência de exemplo produziu um colete com confiança 0,2896 em 3.661,6 ms, incluindo carregamento do modelo; a inferência por imagem já carregada medida pela validação foi 9,1 ms por imagem. Resultados não implicam desempenho em câmeras reais: distância, iluminação, oclusão, objetos pequenos e o treino curto afetam especialmente óculos e capacetes.
