from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.schemas import UserCreateDTO, MeasurementCreateDTO
from app import crud

from app.soup import scrape_books_toscrape

app = FastAPI()
Base.metadata.create_all(engine)


# --- USER ENDPOINT ---
@app.post("/users/")
async def create_user(user: UserCreateDTO, db: Session = Depends(get_db)):
    new_user = await crud.create_user(db, user)
    return {"id": new_user.id}


# --- MEASUREMENT ENDPOINT ---
@app.post("/measurements/")
async def add_measurement(
    user_id: int,
    measurement: MeasurementCreateDTO,
    db: Session = Depends(get_db)
):
    new_measurement = await crud.add_measurement(db, user_id, measurement)

    return {
        "id": new_measurement.id,
        "user_id": new_measurement.user_id,
        "points": [{"x": p.x, "y": p.y} for p in new_measurement.points]
    }


# --- GET MEASUREMENT ---
@app.get("/measurements/{measurement_id}")
async def get_measurement(measurement_id: int, db: Session = Depends(get_db)):
    measurement = await crud.get_measurement(db, measurement_id)

    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")

    return {
        "id": measurement.id,
        "user_id": measurement.user_id,
        "points": [{"x": p.x, "y": p.y} for p in measurement.points]
    }

@app.get("/scrape_books/")
def get_scraped_books(pages: int = 1):
    if pages < 1:
        raise HTTPException(status_code=400, detail="A lapok száma (pages) legalább 1 kell, hogy legyen.")
        
    book_list = scrape_books_toscrape(max_pages=pages)
    
    if not book_list:
        raise HTTPException(status_code=503, detail="Nem sikerült adatokat kinyerni a forrásoldalról.")
        
    return {
        "count": len(book_list),
        "books": book_list
    }
