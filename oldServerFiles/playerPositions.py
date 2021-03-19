import asyncio
import redis

tickrate = 50

red = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)


async def clock():
    await asyncio.sleep(1/tickrate)
    print(tickrate)