import logging
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import Base, engine, get_db
from app.schemas import UserCreateDTO, MeasurementCreateDTO
from app import crud
from app.soup import scrape_books_toscrape

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
Base.metadata.create_all(engine)


@app.post("/users/")
async def create_user(user: UserCreateDTO, db: Session = Depends(get_db)):

    logger.info(f"Kérés érkezett új felhasználó létrehozására: {user.name}")
    try:
        new_user = await crud.create_user(db, user) 
        logger.info(f"Sikeresen létrehozva a felhasználó, ID: {new_user.id}")
        return {"id": new_user.id}
    except SQLAlchemyError as e:
        logger.error(f"Adatbázis hiba történt a felhasználó létrehozása közben: {e}")
        raise HTTPException(status_code=500, detail="Hiba történt az adatbázis művelet során.")
    except Exception as e:
        logger.error(f"Váratlan hiba történt a felhasználó létrehozása közben: {e}")
        raise HTTPException(status_code=500, detail="Belső szerverhiba.")



@app.post("/measurements/")
async def add_measurement(
    user_id: int,
    measurement: MeasurementCreateDTO,
    db: Session = Depends(get_db)
):
    logger.info(f"Kérés érkezett mérés hozzáadására a(z) {user_id} felhasználóhoz.")
    try:
        new_measurement = await crud.add_measurement(db, user_id, measurement)
        logger.info(f"Sikeresen hozzáadva a mérés, ID: {new_measurement.id}, felhasználó: {user_id}")

        return {
            "id": new_measurement.id,
            "user_id": new_measurement.user_id,
            "points": [{"x": p.x, "y": p.y} for p in new_measurement.points]
        }
    except SQLAlchemyError as e:
        logger.error(f"Adatbázis hiba a mérés hozzáadása közben (User ID: {user_id}): {e}")
        raise HTTPException(status_code=500, detail="Hiba történt az adatbázis művelet során.")
    except Exception as e:
        logger.error(f"Váratlan hiba a mérés hozzáadása közben (User ID: {user_id}): {e}")
        raise HTTPException(status_code=500, detail="Belső szerverhiba.")



@app.get("/measurements/{measurement_id}")
async def get_measurement(measurement_id: int, db: Session = Depends(get_db)):
    logger.info(f"Kérés érkezett a(z) {measurement_id} mérés lekérdezésére.")
    try:
        measurement = await crud.get_measurement(db, measurement_id)

        if not measurement:
            logger.warning(f"A(z) {measurement_id} mérés nem található.")
            raise HTTPException(status_code=404, detail="Measurement not found")

        logger.info(f"Sikeresen lekérdezve a(z) {measurement_id} mérés.")
        return {
            "id": measurement.id,
            "user_id": measurement.user_id,
            "points": [{"x": p.x, "y": p.y} for p in measurement.points]
        }
    except SQLAlchemyError as e:
        logger.error(f"Adatbázis hiba a(z) {measurement_id} mérés lekérdezése közben: {e}")
        raise HTTPException(status_code=500, detail="Hiba történt az adatbázis művelet során.")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Váratlan hiba a mérés lekérdezése közben (ID: {measurement_id}): {e}")
        raise HTTPException(status_code=500, detail="Belső szerverhiba.")

@app.get("/scrape_books/")
def get_scraped_books(pages: int = 1):
    logger.info(f"Kérés érkezett könyvek lekaparására {pages} oldalról.")
    if pages < 1:
        logger.warning("Érvénytelen lapok száma: 0 vagy negatív.")
        raise HTTPException(status_code=400, detail="A lapok száma (pages) legalább 1 kell, hogy legyen.")
        
    try:
        book_list = scrape_books_toscrape(max_pages=pages)
        
        if not book_list:
            logger.error(f"Nem sikerült adatokat kinyerni {pages} oldalról.")
            raise HTTPException(status_code=503, detail="Nem sikerült adatokat kinyerni a forrásoldalról.")
            
        logger.info(f"Sikeresen lekaparva {len(book_list)} könyv {pages} oldalról.")
        return {
            "count": len(book_list),
            "books": book_list
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Kivétel a webkaparás során {pages} oldalon: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Hiba történt a webkaparás végrehajtása közben.")