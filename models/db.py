import asyncio
from aiopyql import data

async def db_setup(server):

    #sqlite connection
    server.db = await data.Database.create(
        database="risk_scores",
        cache_enabled=True
    )

    # create table
    await server.db.create_table(
        'scores',
        [
            ('date_detected', str, 'UNIQUE NOT NULL'),
            ('full_name_p1', str),
            ('full_name_p2', str),
            ('score', int)
        ],
        'date_detected',
        cache_enabled=True
    )