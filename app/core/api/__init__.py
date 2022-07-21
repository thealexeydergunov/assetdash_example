from fastapi import APIRouter

from . import portfolio


router = APIRouter(prefix="")
router.include_router(portfolio.router)
