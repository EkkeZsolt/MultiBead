# MultiBead

Ez a projekt egy teljes körű alkalmazás, amely egy **FastAPI** alapú backendet és egy **Streamlit** alapú frontendet tartalmaz. A rendszer lehetővé teszi felhasználók és mérések kezelését, valamint könyvadatok lekaparását (web scraping) egy külső forrásból.

## 🏗 Architektúra

A projekt két fő komponensből áll:

### 1. Backend (FastAPI)
A backend a `run/backend.py` fájlban található, és a következő funkciókat látja el:
- **REST API**: Végpontokat biztosít felhasználók létrehozására, mérések rögzítésére és lekérdezésére.
- **Adatbázis**: SQLAlchemy ORM-et használ az adatok tárolására (alapértelmezetten SQLite `data.db`).
- **Web Scraping**: A `BeautifulSoup` segítségével könyvadatokat gyűjt a `books.toscrape.com` oldalról.

### 2. Frontend (Streamlit)
A frontend a `run/frontend.py` fájlban található, és egy interaktív felületet biztosít:
- **Felhasználói felület**: Lehetővé teszi az API funkcióinak (felhasználó létrehozása, mérés hozzáadása) kényelmes használatát.
- **Adatvizualizáció**: A `Plotly` segítségével megjeleníti a mérések pontjait és a lekapart könyvek ár-eloszlását.
- **Kommunikáció**: HTTP kéréseket küld a backend felé a `requests` könyvtár segítségével.

## 🚀 Indítás

A projekt futtatásához szükség van a Python környezet beállítására és a függőségek telepítésére.

### Előfeltételek
- Python 3.8+
- Virtuális környezet (ajánlott)

### Telepítés

1. Hozd létre és aktiváld a virtuális környezetet (opcionális, de ajánlott):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

2. Telepítsd a függőségeket:
   ```bash
   pip install -r run/requirements.txt
   ```

### Futtatás

A backendet és a frontendet két külön terminálban kell futtatni.

#### 1. Backend indítása
A projekt gyökérkönyvtárából futtasd a következő parancsot:

```bash
uvicorn run.backend:app --reload
```
Ez elindítja a szervert a `http://127.0.0.1:8000` címen.

#### 2. Frontend indítása
Nyiss egy új terminált, aktiváld a virtuális környezetet, majd futtasd:

```bash
streamlit run run/frontend.py
```
Ez megnyitja az alkalmazást a böngészőben (általában a `http://localhost:8501` címen).

## 🛠 Funkciók

- **Felhasználó létrehozása**: Új felhasználó regisztrálása név megadásával.
- **Mérés hozzáadása**: Koordináták (x, y) rögzítése egy adott felhasználóhoz manuálisan vagy fájlból feltöltve.
- **Mérés lekérdezése**: Mérés adatainak és pontjainak megjelenítése grafikonon.
- **Könyv Scraper**: Könyvek adatainak (cím, ár, értékelés) lekaparása és elemzése.

## Vagy egyszerően futtatod a 
   setup.sh vagy setup.ps1
