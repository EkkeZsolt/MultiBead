py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "run.backend:app --reload"
streamlit run run/frontend.py
