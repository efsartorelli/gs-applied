# Arquitetura

`Construction-PPE (CC BY 4.0)` → `prepare_dataset.py` → subconjunto de três classes → `YOLO11n` treinado localmente → `best.pt` → inferência Python/Streamlit.

O recorte remove classes que não pertencem ao objetivo. A interface aceita imagem autorizada e mostra caixas, classe e confiança; há script separado para vídeo. Nenhuma detecção é certificação de segurança, verificação de identidade ou evidência de uso correto do EPI.
