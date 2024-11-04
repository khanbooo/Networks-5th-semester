import asyncio

import requests
from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from dialogueStatuses import DialogueStatuses
from status import Status
from config import GRAPHHOPPER_API_TOKEN
from config import OPENWEATHER_API_TOKEN
from config import OPENTRIPMAP_API_TOKEN
from config import RADIUS

router = Router()
status = Status()


async def go_back(message: Message):
    status.set_status(status.get_upper_status)
    if status.get_status == DialogueStatuses.CHOOSING_LOCATION:
        await message.answer('Введите место, которое хотите найти.')
    elif status.get_status == DialogueStatuses.MAIN_PAGE:
        await message.answer('Введи "/find", чтобы начать поиск.')


async def set_find_location_status(message: Message):
    status.set_status(DialogueStatuses.CHOOSING_LOCATION)
    await message.answer('Введите место, которое хотите найти.')


async def find_location(message: Message):
    url = "https://graphhopper.com/api/1/geocode"

    query = {
        "q": message.text,
        "locale": "ru",
        "limit": "5",
        "provider": "default",
        "key": GRAPHHOPPER_API_TOKEN
    }

    response = requests.get(url, params=query)

    data = response.json()['hits']

    buttons = []

    for location in data:
        # print(f'{location["name"]};{location["country"]};{location["point"]["lat"]};{location["point"]["lng"]}')
        buttons.append([InlineKeyboardButton(text=f'{location["name"]}, {location["country"]}',
                                             callback_data=f'{location["point"]["lat"]};{location["point"]["lng"]}')])
        # await message.answer(location)
    inline_kb = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=5)
    status.set_status(DialogueStatuses.CHOOSING_PLACE)
    await message.reply('Выберите наиболее подходящие под Ваш запрос локации или вернитесь к поиску'
                        ', написав мне "/back".', reply_markup=inline_kb)


async def get_weather(text, lat, lon):
    weather_url = (f"https://api.openweathermap.org/data/2.5/weather?lat="
                   f"{lat}&lon={lon}&appid={OPENWEATHER_API_TOKEN}&lang=ru")
    response = requests.get(weather_url)
    data = response.json()
    text.append(", ".join(["Погода в выбранном месте: " + data['weather'][0]['description'],
                           '{:.1f}'.format(data['main']['temp'] - 273) + "C"]))


async def get_interesting_places(text, lat, lon):
    lang = "ru"
    kinds = "interesting_places"
    limit = 5
    places_url = (f"http://api.opentripmap.com/0.1/{lang}/places/radius?radius={RADIUS}&lon={lon}&lat={lat}"
                  f"&kinds={kinds}&limit={limit}&format=json&apikey={OPENTRIPMAP_API_TOKEN}")
    response = requests.get(places_url)
    data = response.json()
    i = 1
    for place in data:
        name = place['name']
        if name == "":
            continue
        xid = place['xid']
        # print(place['name'], xid)
        description_url = f"http://api.opentripmap.com/0.1/{lang}/places/xid/{xid}?apikey={OPENTRIPMAP_API_TOKEN}"
        description = requests.get(description_url).json()

        # print(f'description = {descr}')
        # if 'info' in description and 'descr' in description['info']:
        #     descr = description['info']['descr']
        #     text.append(f'\n{i}. {name}\n    Описание: {descr}\n')

        if 'wikipedia_extracts' in description:
            descr = description['wikipedia_extracts']['text']
            text.append(f'\n{i}. {name}\n    Описание: {descr}\n')
        else:
            text.append(f'\n{i}. {name}\n')

        i += 1


async def unknown_command(message: Message):
    status.set_status(status.get_upper_status)
    await message.answer('Я не знаю такой команды. Попробуй ещё раз.')


@router.message(CommandStart())
async def start_command(message: Message):
    status.set_status(DialogueStatuses.MAIN_PAGE)
    await message.answer('Я готов к работе! Введи "/find", чтобы начать поиск. '
                         'Чтобы вернуться к предыдущему шагу, введите "/back".')


@router.message()
async def incoming_message(message: Message):
    print(message.text)
    if message.text.lower() == '/back':
        await go_back(message)
        return
    if status.is_main_page:
        if message.text.lower() == '/find':
            await set_find_location_status(message)
        else:
            await unknown_command(message)
    elif status.is_choosing_location:
        await find_location(message)
    else:
        await message.answer('Я не знаю такой команды. Попробуй ещё.')


@router.callback_query()
async def handle_inline_button(callback_query: CallbackQuery):
    weather = []
    places = []
    lat, lon = callback_query.data.split(';')

    weather_coro = asyncio.create_task(get_weather(weather, lat, lon))
    places_coro = asyncio.create_task(get_interesting_places(places, lat, lon))

    await weather_coro
    await places_coro

    # await callback_query.
    await callback_query.message.answer(f'{weather[0]}\n')
    if places:
        # for i in range(len(places)):
        #     text = places[i]
        #     formatted_text = ""
        #     flag = 0
        #     for j in range(len(text)):
        #         if text[j] == '<':
        #             flag = 1
        #         elif text[j] == '>':
        #             flag = 0
        #         else:
        #             if not flag:
        #                 formatted_text += text[j]
        #     places[i] = formatted_text
        await callback_query.message.answer(f'Места, которые обязательно стоит посетить:\n{"".join(places)}')
    else:
        await callback_query.message.answer(f'Достопримечательностей поблизости не найдено\n')
    await callback_query.message.answer('Вы можете продолжить изучение локаций, нажав на одну из кнопок выше, '
                                        'или вернуться к поиску, написав мне "/back".')
    await callback_query.answer()
