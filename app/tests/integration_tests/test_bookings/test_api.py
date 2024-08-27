from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms, status_code",
    [
        (4, "2030-05-01", "2030-05-15", 3, 200),
        (4, "2030-05-01", "2030-05-15", 4, 200),
        (4, "2030-05-01", "2030-05-15", 5, 200),
        (4, "2030-05-01", "2030-05-15", 6, 200),
        (4, "2030-05-01", "2030-05-15", 7, 200),
        (4, "2030-05-01", "2030-05-15", 8, 200),
        (4, "2030-05-01", "2030-05-15", 9, 200),
        (4, "2030-05-01", "2030-05-15", 10, 200),
        (4, "2030-05-01", "2030-05-15", 10, 409),
        (4, "2030-05-01", "2030-05-15", 10, 409),
    ],
)
async def test_add_and_get_booking(
    room_id, date_from, date_to, booked_rooms, status_code, authenticated_ac: AsyncClient
):
    responce = await authenticated_ac.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert responce.status_code == status_code
    
    responce = await authenticated_ac.get("/bookings")
    
    assert len(responce.json()) == booked_rooms
