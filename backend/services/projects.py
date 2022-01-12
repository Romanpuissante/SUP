from typing import Type

from passlib.hash import bcrypt
from fastapi_jwt_auth import AuthJWT

from orm.models import Projects
from orm.schema import BaseProject, UserFull, UserLogin, UserSimple, UserAuth
from .base import BaseServices
from services.dicts import OtdelService, PositionService, RankService
from conf.exeptions import unauthError, usernameError


# class tableFK(object):
#     def __init__(self, db):
#         self.fk = {
#             "otdel": OtdelService(db),
#             "position": PositionService(db),
#             "rank": RankService(db)
#         }

class ProjectService(BaseServices[BaseProject,BaseProject, Projects]):
    @property
    def _table(self) -> Type[Projects]:
        return Projects
    @property
    def _schema(self) -> Type[BaseProject]:
        return BaseProject


    # @property
    # def _tableFK(self) -> tableFK:
    #     return tableFK(self._db_session)