from unittest.mock import AsyncMock
from bot.app.handlers import command_start



async def test_command_start(login_client, db):
    r = await login_client.post("/auth/link")
    res = r.json()
    code = res[0][-6:]
    assert r.status_code == 200
    assert len(code) == 6
    mock_message = AsyncMock()
    mock_message.text = f"/start {code}"
    mock_message.from_user.id = 124151686

    await command_start(db=db, message=mock_message)

    user = await db.user.get_one(telegram_id=124151686)
    assert user is not None



