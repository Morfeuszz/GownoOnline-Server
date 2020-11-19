import time
import asyncio
import enemySpawnController


async def clock():
    while(True):
        await asyncio.sleep(5)
        enemySpawnController.respawn()
        


