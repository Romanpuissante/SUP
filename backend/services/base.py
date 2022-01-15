from orm.models import Otdel, Position, Rank

all_fk: dict = {
    "otdel": Otdel,
    "position": Position,
    "rank": Rank
}

class BaseService():

    async def create_fk(self, into_schema: dict, fks_check: tuple) -> dict:
        """
        Создает форины

        Args:
            into_schema (dict): Ожидаемая схема для создания
            dict_fk (dict): Кортеж ключей

        Returns:
            [dict]: Словарь для создания объекта
        """

        for fk in fks_check:

            model = all_fk[fk]
            res = await model.objects.get_or_create(**into_schema[fk])
            into_schema[fk] = res

        return into_schema