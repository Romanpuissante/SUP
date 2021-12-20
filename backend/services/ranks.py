
from orm.schema import BaseRanks
from orm.models import ranks

from .crud import CRUD


class RanksService(CRUD):
    model = ranks
    schema = BaseRanks
