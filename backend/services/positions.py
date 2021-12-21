
from orm.models import  positions
from orm.schema import BasePositions
from .crud import CRUD


class PositionsService(CRUD):
    model = positions
    schema = BasePositions
