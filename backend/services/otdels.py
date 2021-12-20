
from orm.models import otdels
from orm.schema import BaseOtdel
from .crud import CRUD


class OtdelService(CRUD):
    model = otdels
    schema = BaseOtdel

