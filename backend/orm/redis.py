import asyncio
from types import FunctionType

from aioredis.client import PubSub, Redis
from fastapi import (
    WebSocket,
    WebSocketDisconnect
)

from conf.sessions import get_redis_pool
from conf.log import logger
import json

class RedisWorker:
    """ Обработчик редис запросов """

    @classmethod
    async def create_channels(cls, ws: WebSocket, consumer: FunctionType = None, channels=("main",), save_info: dict=None):

        """ Создает каналы, для ассинхронной отправки сообщений

        Args:
            ws (WebSocket): Клиентский сокет
            consumer (Function): Функция обработки принятого сообщения
            channels (tuple): Список каналов для подключения

        Raises:
            WebSocketDisconnect: [
                Отключение сокета -> 
                отправляяет сообщение для остановки бесконечного цикла и отписывает пользователя от канала
            ]
        """

        conn: Redis = await get_redis_pool()
        if save_info:
            for channel, info in save_info.items():
                await conn.set(channel, json.dumps(info))
        pubsub = conn.pubsub()

        async def consumer_handler(conn: Redis, ws: WebSocket, channels: tuple, save_info: dict):
            """ Публикует каналы в редис

            Args:
                conn (Redis): Подключение редис
                ws (WebSocket): Клиентский сокет
                channels (tuple): Список каналов для подключения
            """
            try:
                while True:
                    message = await ws.receive_text()
                    if message:
                        if consumer:
                            result: dict = await consumer(message, conn)
                        for (channel, answer) in result.items():
                            await conn.publish(channel, answer)

            except WebSocketDisconnect:

                if save_info:
                    for channel in save_info.keys():
                        await conn.delete(channel)
                await conn.publish(channels[0], "StopSocket")
                await conn.close()
                return
                
                
        async def producer_handler(pubsub: PubSub, ws: WebSocket, channels: tuple):
            """ Рассылает сообщение пользователям в зависимости от канала

            Args:
                pubsub (PubSub): Публикации, подписанных на канал 
                ws (WebSocket): Клиентский сокет
                channels (tuple): Список каналов для подключения

            Raises:
                WebSocketDisconnect: кидаем исключение при получение сообщения об отключении сокета
            """
            await pubsub.subscribe(*channels)

            try:
                while True:
                    message = await pubsub.get_message(ignore_subscribe_messages=True)
                    if message:

                        if message.get('data') == "StopSocket":
                            raise WebSocketDisconnect()

                        await ws.send_text(message.get('data'))
                        

            except WebSocketDisconnect:
                await pubsub.unsubscribe()

            except Exception as e:
                logger.exception(e)


        consumer_task = consumer_handler(conn=conn, ws=ws, channels=channels, save_info=save_info)
        producer_task = producer_handler(pubsub=pubsub, ws=ws, channels=channels)
        
        done, pending = await asyncio.wait(
            [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:

            task.cancel()

