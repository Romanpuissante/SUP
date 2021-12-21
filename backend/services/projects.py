from orm.schema import BaseProject
from orm.models import project

from .crud import CRUD


class ProjectService(CRUD):
    model = project
    schema = BaseProject
