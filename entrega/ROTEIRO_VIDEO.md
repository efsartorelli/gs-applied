# Roteiro de demonstração (3–5 minutos sugeridos)

1. Apresente o projeto, a FIAP, a disciplina e o objetivo: localizar visualmente capacete, colete e óculos em imagens autorizadas.
2. Explique o contexto CitizenTech: o Quem Faz é somente a motivação de serviços profissionais; o detector não certifica segurança.
3. Mostre `dataset/README.md`, o mapeamento das três classes e a licença CC BY 4.0.
4. Mostre `docs/TREINAMENTO.md`, a configuração conservadora e a execução customizada no terminal.
5. Mostre `docs/RESULTADOS.md`, curvas, matriz de confusão e o teste independente.
6. Execute `streamlit run src/app.py`, envie uma imagem e explique caixas/confiança. Se houver vídeo autorizado, rode `src/process_video.py` e mostre o MP4 anotado.
7. Feche com limitações: pouca quantidade de épocas, óculos menores/oclusos, iluminação e ausência de certificação.
