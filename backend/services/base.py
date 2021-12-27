import abc
from typing import Generic, TypeVar, Type

from sqlalchemy.ext.asyncio import AsyncSession
from conf.exeptions import doesNotNoteError
from sqlalchemy import select, update, delete

from orm.schema import BaseSchema, BaseOnlyId

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE")

class BaseServices(Generic[IN_SCHEMA, SCHEMA, TABLE], metaclass=abc.ABCMeta):
    """ Сервис, используемый для хранения основным методов загрузки и залития данных в БД
        Обязательно требуется указать таблицу с которой происходит работа и схема данных,
        получаемых на выходе
    """

    def __init__(self, db_session: AsyncSession, *args, **kwargs) -> None:
        self._db_session: AsyncSession = db_session

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        ...

    @property
    def _tableFK(self) -> 'BaseServices':
        ...

    # *Методы помощники
    def set_filter(self, query: select, fields):
        """ Позволяет сконструировать условие where для запроса, приняв в аргументы
            запрос и словарь полей со значениями, по которым нужно отфильтровать запрос    
        """

        for attr, value in fields.items():
            query = query.where(getattr(self._table, attr).like("%%%s%%" % value))
        return query

    # *Основные методы, для работы с простыми таблицами
    async def create(self, in_schema: IN_SCHEMA, out_schema=None) -> SCHEMA:
        """ Создание записи в таблице использую стандартную схему """

        entry = self._table(**in_schema.dict())
        self._db_session.add(entry)
        await self._db_session.commit()

        out_schema = out_schema if out_schema else self._schema
        return out_schema.from_orm(entry)

    async def get(self, entry_id: int) -> SCHEMA:
        """ Взять запись используя id """
        
        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise doesNotNoteError
        return self._schema.from_orm(entry)

    async def all(self):
        """ Забрать все записи """
        result = await self._db_session.execute(select(self._table))
        await self._db_session.commit()
        return [self._schema.from_orm(row) for row in result.scalars()]

    async def update(self, entry_id: int, in_schema: IN_SCHEMA):
        """ Обновить одну запись """

        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise doesNotNoteError

        query = update(self._table).where(self._table.id == entry_id).values(**in_schema.dict())
        await self._db_session.execute(query)
        await self._db_session.commit()
        return {"msg": "Запись успешно обновлена"}

    async def delete(self, entry_id):
        """ Удалить одну запись по id """

        entry = await self._db_session.get(self._table, entry_id)
        if not entry:
            raise doesNotNoteError
        await self._db_session.delete(entry)
        return {"msg": "Запись успешно удалена"}

    async def delete_all(self):
        """ Удалить все записи """
        
        await self._db_session.execute(delete(self._table))
        await self._db_session.commit()
        return {"msg": "Все записи успешно удалены"}

    # *Расширенные методы
    async def get_with_filter(self, fields: dict, out_schema=None) -> SCHEMA:
        """ 
        Используется, чтобы взять одну запись используя указанный ключ или составной, если указано больще одного поля в словаре
        fields - Словарь полей и значений фильтрации, 
        custom_schema - если надо изменить схему для выхода данных 
        """

        query = self.set_filter(select(self._table), fields)
        result = (await self._db_session.execute(query)).scalars().first()
        await self._db_session.commit()

        if result == None:
            return None

        out_schema = out_schema if out_schema else self._schema
        return out_schema.from_orm(result)

    async def check_foreign_key(self, in_schema):
        """ Проверяет наличие вторичного ключа в базе и редактирует принятую схему,
            записав id в нужные поля для создания корректной записи в таблице.
            Прежде, чем использовать, ожидает в классе ребенке наличия вспомогательного класса,
            который содержит в себе необходимые сервисы для создания FK
            
            Пример:
            class tableFK(object):
            def __init__(self, db):
                self.fk = {
                    "otdel": OtdelService(db),
                    "position": PositionService(db),
                    "rank": RankService(db)
                }

            Внутри ребенка:
            @property
            def _tableFK(self) -> tableFK:
                return tableFK(self._db_session)

            Требуется для корректного создания зависимостей и использования внутри одной сессии

            in_schema - входные данные, содержащие информацию для создания записи
            models - для корректной работы надо передать список ключей

            Возвращает исправленную схему, готовую для записи.
        """
        fk: dict = getattr(self._tableFK, "fk")
        service: 'BaseServices'
        ready_schema = in_schema.dict()

        for key, service in fk.items():

            current_schema = getattr(in_schema, key)
            if not current_schema:
                continue

            note = await service.get_with_filter(current_schema.dict(), BaseOnlyId)
    
            if not note:
                note = await service.create(current_schema, BaseOnlyId)

            del ready_schema[key]
            ready_schema[f"{key}_id"] = note.id

        return ready_schema


    


