from schemas import UserCreateDTO, MeasurementCreateDTO, MeasurementPointDTO
from crud import create_user, add_measurement
import random
import math

def test_data():

    u16 = create_user(UserCreateDTO(name="Quinn"))
    create_big_test_measurement(u16.id)


    u17 = create_user(UserCreateDTO(name="Adam"))
    create_big_test_measurement(u17.id)


    u18 = create_user(UserCreateDTO(name="Thomas"))
    create_big_test_measurement(u18.id)


    u19 = create_user(UserCreateDTO(name="Sophia"))
    create_big_test_measurement(u19.id)


    u20 = create_user(UserCreateDTO(name="Samuel"))
    create_big_test_measurement(u20.id)


def create_big_test_measurement(user_id: int, n_points: int = 1000):


    points = []

    for i in range(n_points):
        x = i / 10                       
        y = (
            10 * math.sin(i / 30) +       
            5 * math.sin(i / 7) +         
            random.uniform(-1, 1)         
        )
        points.append(MeasurementPointDTO(x=x, y=y))

    measurement = add_measurement(
        user_id,
        MeasurementCreateDTO(points=points)
    )

    return measurement
