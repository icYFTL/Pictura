from core import dp, bot
from aiogram.types import Message
from source.telegram.objects.event import Event
from source.database.methods import *
from source.database.user import User
from source.telegram.keyboard import *
from source.vk.api import VkApi as VK
import io
from threading import Thread

events = set()


def get_user_event(id: int) -> Event:
    return [x for x in events if x.telegram_id == id][0] if events else None


def add_event(event: Event) -> None:
    events.add(event)


def del_event(id=None, event=None) -> None:
    if not id and not event:
        return
    try:
        if event:
            events.remove(event)
        else:
            events.remove(get_user_event(id))
    except:
        pass


@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer(text=msg['on_start'], parse_mode='markdownV2')
        add_event(Event(telegram_id=message.from_user.id, type='get_access'))
    else:
        await message.answer(text=msg['also_know'], reply_markup=collect_new_pack())


@dp.message_handler(regexp='^Collect$')
async def collect_one(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer(msg['register_first'])
        return
    await message.answer(msg['send_sticker'])
    add_event(Event(telegram_id=message.from_user.id, type='await_sticker'))


@dp.message_handler(regexp='^Cancel$')
async def on_cancel(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer(msg['register_first'])
        return
    del_event(user.tg_id)
    await message.answer('Canceled')


@dp.message_handler()
async def on_any(message: Message):
    user = get_user(message.from_user.id)
    if not user:
        await message.answer(msg['register_first'])
        return
    event: Event = get_user_event(message.from_user.id)
    if event:
        if event.type == 'get_access':
            from source.vk.api import VkApi
            if VkApi.is_token_valid(message.text):
                add_user(User(token=message.text, tg_id=message.from_user.id))
                del_event(id=message.from_user.id)
                await message.answer(text=msg['on_good_token'], reply_markup=collect_new_pack())
            else:
                await message.answer(text=msg['on_bad_token'])
        elif event.type == 'await_sticker':
            name = message.text.replace('https://t.me/addstickers/', '')
            try:
                await bot.get_sticker_set(name)
            except:
                await message.answer('Invalid sticker pack.\nTry again.')
                return
            del_event(message.from_user.id)
            add_event(Event(telegram_id=message.from_user.id, type='await_album_name', collection_name=name))
            await message.answer(msg['give_album_name'].format(name=name))
        elif event.type == 'await_album_name':
            name = message.text if message.text != 'y' else event.objects['collection_name']
            if len(name) < 3:
                await message.answer('Invalid album name\nName must be longer 2 symbols')
                return
            event = get_user_event(message.from_user.id)
            stickers = await bot.get_sticker_set(event.objects['collection_name'])
            io_stickers = list()
            await message.answer(msg['transfer_started'])
            del_event(message.from_user.id)
            for sticker in stickers.values['stickers']:
                io_object = io.BytesIO()
                await bot.download_file_by_id(sticker.file_id, io_object)
                io_stickers.append(io_object)
            Thread(target=transfer, args=(io_stickers, name, user)).start()


def transfer(io_stickers, album_name, user):
    VK(token=user.token).transfer(
        collection=io_stickers,
        album_name=album_name
    )
