
from aiogram import Router

from .start import start_router
from .mykolaiv import mykolaiv_router


root_router = Router()
root_router.include_routers(
    start_router,
    mykolaiv_router,
)

