
import requests
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


mykolaiv_router = Router()

timeseries = {
    1: [0.0, "00:00:00", "00:30:00"],
    2: [0.5, "00:30:00", "01:00:00"],
    3: [1.0, "01:00:00", "01:30:00"],
    4: [1.5, "01:30:00", "02:00:00"],
    5: [2.0, "02:00:00", "02:30:00"],
    6: [2.5, "02:30:00", "03:00:00"],
    7: [3.0, "03:00:00", "03:30:00"],
    8: [3.5, "03:30:00", "04:00:00"],
    9: [4.0, "04:00:00", "04:30:00"],
    10: [4.5, "04:30:00", "05:00:00"],
    11: [5.0, "05:00:00", "05:30:00"],
    12: [5.5, "05:30:00", "06:00:00"],
    13: [6.0, "06:00:00", "06:30:00"],
    14: [6.5, "06:30:00", "07:00:00"],
    15: [7.0, "07:00:00", "07:30:00"],
    16: [7.5, "07:30:00", "08:00:00"],
    17: [8.0, "08:00:00", "08:30:00"],
    18: [8.5, "08:30:00", "09:00:00"],
    19: [9.0, "09:00:00", "09:30:00"],
    20: [9.5, "09:30:00", "10:00:00"],
    21: [10.0, "10:00:00", "10:30:00"],
    22: [10.5, "10:30:00", "11:00:00"],
    23: [11.0, "11:00:00", "11:30:00"],
    24: [11.5, "11:30:00", "12:00:00"],
    25: [12.0, "12:00:00", "12:30:00"],
    26: [12.5, "12:30:00", "13:00:00"],
    27: [13.0, "13:00:00", "13:30:00"],
    28: [13.5, "13:30:00", "14:00:00"],
    29: [14.0, "14:00:00", "14:30:00"],
    30: [14.5, "14:30:00", "15:00:00"],
    31: [15.0, "15:00:00", "15:30:00"],
    32: [15.5, "15:30:00", "16:00:00"],
    33: [16.0, "16:00:00", "16:30:00"],
    34: [16.5, "16:30:00", "17:00:00"],
    35: [17.0, "17:00:00", "17:30:00"],
    36: [17.5, "17:30:00", "18:00:00"],
    37: [18.0, "18:00:00", "18:30:00"],
    38: [18.5, "18:30:00", "19:00:00"],
    39: [19.0, "19:00:00", "19:30:00"],
    40: [19.5, "19:30:00", "20:00:00"],
    41: [20.0, "20:00:00", "20:30:00"],
    42: [20.5, "20:30:00", "21:00:00"],
    43: [21.0, "21:00:00", "21:30:00"],
    44: [21.5, "21:30:00", "22:00:00"],
    45: [22.0, "22:00:00", "22:30:00"],
    46: [22.5, "22:30:00", "23:00:00"],
    47: [23.0, "23:00:00", "23:30:00"],
    48: [23.5, "23:30:00", "00:00:00"],
}
queues = {
    "1.1": 14,
    "1.2": 15,
    "2.1": 16,
    "2.2": 17,
    "3.1": 19,
    "3.2": 20,
    "4.1": 21,
    "4.2": 22,
    "5.1": 24,
    "5.2": 25,
    "6.1": 26,
    "6.2": 27
}
status = {
    "off": "🔴",
    "probably_off": "🟡",
    "sure_off": "⚠️"
}


def get_next_outage_for_selected(queue: str):
    response = requests.get(
        url="https://off.energy.mk.ua/api/v2/schedule/active",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }
    )

    queue_id = queues[queue]

    data = response.json()

    day = data[0]
    series = day["series"]

    parts = {}

    for row in series:
        if row["outage_queue_id"] != queue_id:
            continue

        hours, start_time, end_time = timeseries[row['time_series_id']]

        parts.update(
            {hours: f"{start_time} - {end_time}: {status[row['type'].lower()]}"}
        )

    keys = sorted(parts)
    new_parts = []

    for key in keys:
        new_parts.append(parts[key])

    return '\n'.join(new_parts)


@mykolaiv_router.callback_query(F.data == "mykolaiv")
async def mykolaiv_queue(callback: CallbackQuery,):
    keyboard = InlineKeyboardBuilder()
    for queue in queues:
        keyboard.row(
            InlineKeyboardButton(
                text=queue,
                callback_data=f"mykolaivq:{queue}"
            )
        )

    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"start"
        )
    )

    await callback.message.edit_text(
        text=f"hello choose your queue",
        parse_mode="html",
        reply_markup=keyboard.as_markup()
    )


@mykolaiv_router.callback_query(F.data.startswith("mykolaivq"))
async def mykolaiv_callback(callback: CallbackQuery):
    queue = callback.data.split(":")[1]
    schedule = get_next_outage_for_selected(queue)

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Back",
            callback_data="mykolaiv",
        )
    )
    await callback.message.edit_text(
        text=f"Група: {queue}"
             f"\n<code>{schedule}</code>",
        reply_markup=keyboard.as_markup(),
        parse_mode="html"
    )

    await callback.answer()
