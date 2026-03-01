# Prensa hidráulica — Simulación (Streamlit)

Pequeña app en Streamlit que simula una prensa hidráulica (principio de Pascal + conservación de volumen).

Requisitos
- Python 3.8+
- Dependencias: `streamlit`, `matplotlib`, `numpy` (ver `requirements.txt`).

Ejecutar localmente
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Subir a GitHub
1. Crea un repositorio en GitHub.
2. En tu máquina (desde la carpeta del proyecto):
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USER/REPO.git
git push -u origin main
```
Reemplaza `https://github.com/USER/REPO.git` por la URL de tu repo.

Desplegar en Streamlit Community Cloud (recomendado)
1. Ve a https://share.streamlit.io y conéctate con GitHub.
2. Click "New app" → elige el repo y la rama `main` y el path `app.py`.
3. Deploy: Streamlit usará `requirements.txt` para instalar dependencias.

Desplegar en Render (opcional)
- Start command: `streamlit run app.py --server.port $PORT --server.headless true`
- Render detectará `requirements.txt` y hará `pip install -r requirements.txt`.

Notas
- GitHub Pages no sirve para apps Streamlit (solo sitios estáticos).
- Si quieres, puedo ejecutar los comandos `git` para crear el repo remoto y pushear: dime la URL del repo y autorizas que lo intente desde aquí.