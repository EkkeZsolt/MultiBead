from .database import SessionLocal
from .models import User, Measurement, MeasurementPoint
from .schemas import MeasurementCreateDTO, UserCreateDTO


async def create_user(session ,data: UserCreateDTO):
    user = User(name=data.name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


async def add_measurement(session,user_id: int, data: MeasurementCreateDTO):

    m = Measurement(user_id=user_id)
    session.add(m)
    session.flush()

    for point in data.points:
        mp = MeasurementPoint(
            x=point.x,
            y=point.y,
            measurement_id=m.id
        )
        session.add(mp)

    session.commit()
    session.refresh(m)
    return m


async def get_measurement(session,measurement_id: int):
    return session.query(Measurement).filter_by(id=measurement_id).first()
