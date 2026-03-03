
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="mykolaiv",
            callback_data="mykolaiv"
        )
    )

    await message.reply(
        text=f"hello choose your city",
        parse_mode="html",
        reply_markup=keyboard.as_markup()
    )


@start_router.callback_query(F.data == "start")
async def start(callback: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="mykolaiv",
            callback_data="mykolaiv"
        )
    )

    await callback.message.edit_text(
        text=f"hello choose your city",
        parse_mode="html",
        reply_markup=keyboard.as_markup()
    )
