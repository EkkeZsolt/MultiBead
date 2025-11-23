from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="measurements")

    points: Mapped[list["MeasurementPoint"]] = relationship(
        back_populates="measurement",
        cascade="all, delete-orphan"
    )


class MeasurementPoint(Base):
    __tablename__ = "measurement_points"

    id: Mapped[int] = mapped_column(primary_key=True)

    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)

    measurement_id: Mapped[int] = mapped_column(ForeignKey("measurements.id"))
    measurement: Mapped["Measurement"] = relationship(back_populates="points")
