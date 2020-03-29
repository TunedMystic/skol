import pytest


@pytest.mark.asyncio
async def test__db_check(conn):
    row = await conn.fetchrow("select 'hello there' as message;")
    assert row['message'] == 'hello there'


@pytest.mark.asyncio
async def test__db__insert_users(conn):
    await conn.execute('''
        insert into _user(name, email)
        values
            ('alice', 'alice.ann@company.com'),
            ('bob', 'bob.brown@company.com');
    ''')
    row = await conn.fetchrow('select count(*) from _user;')
    assert row['count'] == 2


@pytest.mark.asyncio
async def test__db__insert_user(conn):
    await conn.execute('''
        insert into _user(name, email)
        values
            ('dan', 'dan.donovan@company.com');
    ''')
    row = await conn.fetchrow('select count(*) from _user;')
    assert row['count'] == 1
