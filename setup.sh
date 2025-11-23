#!/bin/bash
python3.13 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
nohup uvicorn backend:app --reload > backend.log 2>&1 &
streamlit run streamlit_app.py
