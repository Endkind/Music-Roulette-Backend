from fastapi import APIRouter

from .lobby import router as lobby_router

router = APIRouter(prefix="/v1")
router.include_router(lobby_router)
