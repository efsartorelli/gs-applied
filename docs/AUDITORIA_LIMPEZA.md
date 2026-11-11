# Auditoria de reorganização do repositório

Data da reorganização: 11/11/2026.

## Salvaguarda

Antes da mudança de escopo, foi criado o backup local `C:\Users\EnzoPC\Documents\FIAP\GS-APPLIED_BACKUP_PRE_CV_20261111_1555`. A cópia registrou 41.889 arquivos regulares, aproximadamente 6,93 GB. O Robocopy reportou uma advertência em uma junção de logs temporários do Docker/Airflow; não houve falha relatada para arquivos regulares. Foram conferidos SHA-256 idênticos para o PDF do desafio (`50506C2FEA8953DED97A4BC6DB83A20AE4181A2739CF64AB0D76A401105E8E44`) e para o zip Construction-PPE (`E5817AA9C73F33E525D76CA6BC6AF4E4EAC9DCEA9BCFEF1CFD1A71C09FBC1232`).

## Escopo entregue

O conteúdo versionável foi reorganizado exclusivamente para Applied Computer Vision: preparação do dataset, treinamento, validação, peso, MVP Streamlit, testes, métricas, evidências e documentação. Componentes anteriores de backend, banco, frontend, infraestrutura, RPA, LLM, Airflow, Databricks e Maker não participam da árvore versionada desta entrega.

Alguns diretórios locais ignorados podem permanecer no disco por serem artefatos de execução ou estarem em uso. Eles não entram no Git; o backup externo preserva o estado anterior. Nenhum container ou aplicativo do usuário foi encerrado durante esta reorganização.
