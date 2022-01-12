from fastapi import APIRouter

from . import (
    test,
    auth,
    project
)

router = APIRouter()
router.include_router(test.router)
# router.include_router(users.router)
router.include_router(auth.router)
# router.include_router(project.router)
