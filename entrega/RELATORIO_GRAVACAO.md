# Relatório de gravação

- Data: 11/11/2026.
- Aplicação: `http://127.0.0.1:8501`.
- Ferramentas: Streamlit, Playwright com Microsoft Edge e FFmpeg fornecido por `imageio-ffmpeg`.
- Modelo carregado: `models/best.pt`, YOLO11n treinado para capacete, colete e oculos.
- Entradas reais: `ultralytics-ppe-nov2026-705.jpg` (capacete/colete), `ultralytics-ppe-nov2026-546.jpg` (colete), `ultralytics-ppe-nov2026-625.jpg` (oculos) e `source-3dec6deaf0d256258b125015a036bb67.jpg` (múltiplos objetos).
- Execução: cada imagem foi enviada pelo controle de upload real do Streamlit; a automação clicou em **Detectar EPIs**, aguardou a contagem de detecções e posicionou o resultado anotado no viewport. Não foram usados frames pré-renderizados como saída da interface.
- Arquivo final: `entrega/VIDEO_DEMONSTRACAO_APPLIED_COMPUTER_VISION.mp4`.
- Evidência bruta: `entrega/VIDEO_DEMONSTRACAO_ORIGINAL.webm`.
- Validação técnica: 2min47,43s; H.264 High, `yuv420p`, 1280×720, 30 fps. A decodificação integral com `ffmpeg -v error -i <arquivo> -f null -` retornou sucesso.
- Evidências visuais: `entrega/evidencias_video/` e `entrega/VALIDACAO_VIDEO.json`.
- Limitações: vídeo sem narração; os cards de abertura, resultados e conclusão contextualizam a demonstração. As caixas, classes, contagens e probabilidades foram produzidas pelo modelo em sessão real.
