py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "backend:app --reload"
streamlit run streamlit_app.py
