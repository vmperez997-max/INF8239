from pathlib import Path
import json
import joblib
import streamlit as st

ROOT=Path(__file__).resolve().parents[1]
st.set_page_config(page_title='Sentimiento · INF8239')
st.title('Explorar una predicción de sentimiento')
st.caption('Modelo educativo entrenado con reseñas en inglés de Amazon, IMDb y Yelp.')
st.warning('La etiqueta es una predicción, no una verdad. No validado para español, ironía, opiniones neutrales ni otros dominios.')
path=ROOT/'models/text_model.joblib'
if not path.exists():
    st.error('Falta el modelo. Ejecute scripts/train_text.py antes de iniciar la aplicación.')
    st.stop()

@st.cache_resource
def load_model():
    return joblib.load(path)

text=st.text_area('Reseña en inglés',placeholder='The service was excellent.')
if st.button('Predecir'):
    if not text.strip():
        st.info('Escribe una reseña antes de predecir.')
    else:
        model=load_model()
        features=model.named_steps['tfidf'].transform([text])
        if features.nnz==0:
            st.warning('No se encontraron términos conocidos. La predicción no es informativa; prueba una reseña en inglés.')
        else:
            label=int(model.predict([text])[0])
            st.write('Predicción: '+('Positivo' if label==1 else 'Negativo'))
            st.caption('Revise contexto y negaciones. No usar esta salida para decisiones sobre personas.')

