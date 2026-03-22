from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.crud import get_or_create_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession):
    user = await get_or_create_user(session, message.from_user.id, message.from_user.username)
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я бот-помощник. Вот что я умею:\n"
        "/add <текст> — добавить задачу\n"
        "/tasks — показать список задач\n"
        "/done <номер> — отметить задачу выполненной\n"
        "/help — помощь"
    )