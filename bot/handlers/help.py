from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📚 Справка:\n\n"
        "/start — начать работу\n"
        "/add <текст> — добавить задачу\n"
        "/tasks — показать список задач\n"
        "/done <номер> — отметить задачу выполненной\n"
        "/help — показать эту справку"
    )