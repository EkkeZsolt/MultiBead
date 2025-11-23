import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# FŐ ALKALMAZÁS KÓDJÁNAK IMPORTÁLÁSA
# Feltételezve, hogy a backend.py a 'run' csomag része
from run.backend import app, get_db

# --- Mock Objektumok és Adatok ---

# JAVÍTÁS: 'email' helyett 'name', mert a User modellben name van
TEST_USER_CREATE = {"name": "Teszt Elek"} 

TEST_MEASUREMENT_CREATE = {"points": [{"x": 1.0, "y": 2.0}, {"x": 3.0, "y": 4.0}]}

class MockUser:
    def __init__(self, id, name):
        self.id = id
        self.name = name  # JAVÍTÁS: email helyett name

class MockPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockMeasurement:
    def __init__(self, id, user_id, points_data):
        self.id = id
        self.user_id = user_id
        # A pontok MockPoint objektumként tárolódnak
        self.points = [MockPoint(x=p["x"], y=p["y"]) for p in points_data]


# Mock a get_db függőség-befecskendezéshez
def override_get_db():
    """Felülírja a get_db függőséget a tesztekhez."""
    try:
        db = MagicMock(spec=Session)
        yield db
    finally:
        pass

# Felülírjuk az app get_db függőségét
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- FAKTA TESZTEK ---

## 👥 Felhasználó Végpont Tesztek

@patch('run.backend.crud.create_user') 
def test_create_user_success(mock_create_user):
    """Sikeres felhasználó létrehozás tesztelése (200)."""
    # JAVÍTÁS: Mockoljuk a sikeres DB visszatérést a 'name' mezővel
    mock_create_user.return_value = MockUser(id=1, name=TEST_USER_CREATE["name"])
    
    response = client.post("/users/", json=TEST_USER_CREATE)
    
    # Debug: Ha még mindig hiba van, írjuk ki a választ
    if response.status_code != 200:
        print(f"HIBA VÁLASZ: {response.json()}")

    assert response.status_code == 200
    assert response.json() == {"id": 1}
    mock_create_user.assert_awaited_once()

@patch('run.backend.crud.create_user')
def test_create_user_db_error(mock_create_user):
    """Adatbázis hiba tesztelése (500)."""
    # Mockoljuk a DB hibát
    mock_create_user.side_effect = SQLAlchemyError("Mock DB Error")
    
    response = client.post("/users/", json=TEST_USER_CREATE)
    
    assert response.status_code == 500
    assert "Hiba történt az adatbázis művelet során." in response.json().get("detail")
    mock_create_user.assert_awaited_once()

## 📈 Mérés Hozzáadása Végpont Tesztek

@patch('run.backend.crud.add_measurement') 
def test_add_measurement_success(mock_add_measurement):
    """Sikeres mérés hozzáadás tesztelése (200)."""
    user_id = 1
    # Mockoljuk a sikeres DB visszatérést
    mock_measurement = MockMeasurement(
        id=101, 
        user_id=user_id, 
        points_data=TEST_MEASUREMENT_CREATE["points"]
    )
    mock_add_measurement.return_value = mock_measurement

    response = client.post(f"/measurements/?user_id={user_id}", json=TEST_MEASUREMENT_CREATE)
    
    assert response.status_code == 200
    assert response.json()["id"] == 101
    mock_add_measurement.assert_awaited_once()

## 🔍 Mérés Lekérdezése Végpont Tesztek

@patch('run.backend.crud.get_measurement')
def test_get_measurement_success(mock_get_measurement):
    """Sikeres mérés lekérdezés tesztelése (200)."""
    measurement_id = 101
    # Mockoljuk a sikeres DB visszatérést
    mock_measurement = MockMeasurement(
        id=measurement_id, 
        user_id=1, 
        points_data=TEST_MEASUREMENT_CREATE["points"]
    )
    mock_get_measurement.return_value = mock_measurement
    
    response = client.get(f"/measurements/{measurement_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == measurement_id
    mock_get_measurement.assert_awaited_once()

@patch('run.backend.crud.get_measurement')
def test_get_measurement_not_found(mock_get_measurement):
    """Nem létező mérés (404) tesztelése."""
    measurement_id = 999
    mock_get_measurement.return_value = None
    
    response = client.get(f"/measurements/{measurement_id}")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Measurement not found"}
    mock_get_measurement.assert_awaited_once()

## 🕷️ Webkaparás Végpont Tesztek

# Feltételezve, hogy a scrape_books_toscrape a backend.py-ban van importálva
@patch('run.backend.scrape_books_toscrape') 
def test_scrape_books_success(mock_scrape_books):
    """Sikeres webkaparás tesztelése (200)."""
    mock_books = [{"title": "Book 1", "price": 10.0}, {"title": "Book 2", "price": 20.0}]
    mock_scrape_books.return_value = mock_books
    
    response = client.get("/scrape_books/?pages=1")
    
    assert response.status_code == 200
    assert response.json()["count"] == 2
    mock_scrape_books.assert_called_once_with(max_pages=1)

@patch('run.backend.scrape_books_toscrape')
def test_scrape_books_invalid_pages(mock_scrape_books):
    """Érvénytelen (negatív) lapok száma (400) tesztelése."""
    response = client.get("/scrape_books/?pages=0")
    
    assert response.status_code == 400
    assert "A lapok száma (pages) legalább 1 kell, hogy legyen." in response.json().get("detail")
    mock_scrape_books.assert_not_called()

@patch('run.backend.scrape_books_toscrape')
def test_scrape_books_general_exception(mock_scrape_books):
    """Általános hiba tesztelése webkaparás közben (500)."""
    mock_scrape_books.side_effect = Exception("Mock Web Scraping Error")
    
    response = client.get("/scrape_books/?pages=1")
    
    assert response.status_code == 500
    assert "Hiba történt a webkaparás végrehajtása közben." in response.json().get("detail")
    mock_scrape_books.assert_called_once()