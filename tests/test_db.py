import pytest


@pytest.mark.asyncio
async def test__db_check(db):
    row = await db.fetch_one("select 'hello there' as message;")
    assert row['message'] == 'hello there'
