from typing import Type

from .base import BaseServices
from orm.schema import (
    OtdelSimple,
    OtdelFull,
    PositionSimple,
    PositionFull,
    RankSimple,
    RankFull
)
from orm.models import Otdel, Position, Rank

class OtdelService(BaseServices[OtdelSimple, OtdelFull, Otdel]):

    @property
    def _in_schema(self) -> Type[OtdelFull]:
        return OtdelSimple

    @property
    def _schema(self) -> Type[OtdelFull]:
        return OtdelFull

    @property
    def _table(self) -> Type[Otdel]:
        return Otdel

class PositionService(BaseServices[PositionSimple, PositionFull, Position]):

    @property
    def _in_schema(self) -> Type[PositionFull]:
        return PositionSimple

    @property
    def _schema(self) -> Type[PositionFull]:
        return PositionFull

    @property
    def _table(self) -> Type[Position]:
        return Position

class RankService(BaseServices[RankSimple, RankFull, Rank]):

    @property
    def _in_schema(self) -> Type[RankFull]:
        return RankSimple

    @property
    def _schema(self) -> Type[RankFull]:
        return RankFull

    @property
    def _table(self) -> Type[Rank]:
        return Rank



