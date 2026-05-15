from src.services.auth import Auth
import pytest

@pytest.mark.parametrize("email, password", [
    ("gooddog@gmail.com", "qwerty1234"),
    ("cat123@mail.de", "cat321123"),
    ("manmail@mail.com", "qwerty1234"),
])
async def test_user_crud(email, password, ac):
    reg_user = await ac.post("/auth/register", json={"email": email, "password": password})
    assert reg_user.status_code == 200

    log_user = await ac.post("/auth/login", json={"email": email, "password": password})
    assert log_user.status_code == 200
    res = log_user.cookies["access_token"]
    assert res is not None
    print(res)
    assert "access_token" in log_user.json()

    logout_user = await ac.post("/auth/logout")
    assert logout_user.status_code == 200
    print(logout_user.cookies)
    assert "access_token" not in logout_user.json()