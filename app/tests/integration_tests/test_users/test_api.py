from typing import Literal
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("kot@pes.com", "kotopes", 200),
        ("kot@pes.com", "kot0pes", 409),
        ("pes@kot.com", "pesokot", 200),
        ("abcde", "kotopes", 422),
    ],
)
async def test_register_user(
    email: Literal["kot@pes.com", "pes@kot.com", "abcde"],
    password: Literal["kotopes", "kot0pes", "pesokot"],
    status_code: Literal[200, 409, 422],
    ac: AsyncClient,
):
    responce = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert responce.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", "test", 200),
        ("artem@example.com", "artem", 200),
        ("wtong@person.com", "artem", 401)
    ],
)
async def test_login_user(
    email: Literal["test@test.com", "artem@example.com", "artem@example.com"],
    password: Literal["test", "artem"],
    status_code: Literal[200, 401],
    ac: AsyncClient,
):
    responce = await ac.post("/auth/login", json={"email": email, "password": password})
    assert responce.status_code == status_code
