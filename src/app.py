"""Interface Streamlit dedicada à demonstração de detecção de EPI."""
from pathlib import Path
import tempfile
import cv2
import streamlit as st
from PIL import Image
import numpy as np
from detect import CLASS_NAMES, detect, load_model, model_path

st.set_page_config(page_title='EPI Vision | Quem Faz',page_icon='🦺',layout='wide')
st.title('Detecção Inteligente de EPIs')
st.caption('Applied Computer Vision · Global Solution 2026.2 · Contexto conceitual: Quem Faz')
st.info('Detecta visualmente capacete, colete e óculos. É uma demonstração educacional e não certifica segurança, conformidade ou uso adequado de EPI.')
st.write('Classes treinadas:', ', '.join(CLASS_NAMES))

@st.cache_resource
def ready_model(): return load_model()

try:
    ready_model(); st.success(f'Modelo carregado: {model_path().name}')
except Exception as error:
    st.error(str(error)); st.stop()

tab_image,tab_video=st.tabs(['Imagem','Vídeo'])
with tab_image:
    upload=st.file_uploader('Envie uma imagem autorizada',type=['jpg','jpeg','png','webp'],key='image')
    confidence=st.slider('Confiança mínima',0.05,0.95,0.25,0.05)
    if upload:
        original=np.array(Image.open(upload).convert('RGB'))
        model_input=cv2.cvtColor(original,cv2.COLOR_RGB2BGR)
        if st.button('Detectar EPIs',type='primary'):
            with st.spinner('Executando inferência local...'):
                annotated,detections,elapsed=detect(model_input,confidence,model=ready_model())
            left,right=st.columns(2); left.image(original,caption='Imagem enviada'); right.image(annotated,channels='BGR',caption='Detecções')
            st.write(f'{len(detections)} detecção(ões) · {elapsed} ms')
            st.dataframe(detections,use_container_width=True)
with tab_video:
    video=st.file_uploader('Envie vídeo curto para processamento local',type=['mp4','avi','mov'],key='video')
    if video:
        st.video(video)
        st.caption('Para preservar recursos no navegador, processe vídeos pelo comando `python src/process_video.py --input arquivo.mp4`. O script gera um MP4 anotado para a demonstração.')
