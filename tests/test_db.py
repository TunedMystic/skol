import pytest


@pytest.mark.asyncio
async def test__db_check(conn):
    row = await conn.fetchrow("select 'hello there' as message;")
    assert row['message'] == 'hello there'
