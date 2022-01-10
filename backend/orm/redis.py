import asyncio
from types import FunctionType

from aioredis.client import PubSub, Redis
from fastapi import (
    WebSocket,
    WebSocketDisconnect
)

from conf.sessions import get_redis_pool
from loguru import logger

class RedisWorker:

    @classmethod
    async def create_channels(cls, ws: WebSocket, consumer: FunctionType, channels=("main",)):

        conn: Redis = await get_redis_pool()
        pubsub = conn.pubsub()

        async def consumer_handler(conn: Redis, ws: WebSocket, channels: tuple):
            try:
                while True:
                    message = await ws.receive_text()
                    if message:
                        result: dict = await consumer(message)
                        for (channel, answer) in result.items():
                            await conn.publish(channel, answer)

            except WebSocketDisconnect as exc:
                # TODO this needs handling better

                await conn.publish(channels[0], "StopIter")
                return await conn.close()
                
                
        async def producer_handler(pubsub: PubSub, ws: WebSocket, channels: tuple):
            
            await pubsub.subscribe(*channels)

            try:
                
                while True:
                    message = await pubsub.get_message(ignore_subscribe_messages=True)
                    if message:

                        if message.get('data') == "StopIter":
                            raise WebSocketDisconnect()

                        await ws.send_text(message.get('data'))
                        


            except WebSocketDisconnect as e:
                # TODO this needs handling better
                logger.info("Соединение закрыто")
                await pubsub.unsubscribe()
        

        consumer_task = consumer_handler(conn=conn, ws=ws, channels=channels)
        producer_task = producer_handler(pubsub=pubsub, ws=ws, channels=channels)
        
        done, pending = await asyncio.wait(
            [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:

            task.cancel()

