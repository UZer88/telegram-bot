from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.crud import add_task, get_tasks, mark_task_done, get_or_create_user

router = Router()


@router.message(Command("add"))
async def cmd_add(message: types.Message, session: AsyncSession):
    text = message.text.replace("/add", "").strip()
    if not text:
        await message.answer("❌ Напишите задачу после команды: /add купить молоко")
        return

    user = await get_or_create_user(session, message.from_user.id, message.from_user.username)
    task = await add_task(session, user.id, text)
    await message.answer(f"✅ Задача добавлена: {task.title}")


@router.message(Command("tasks"))
async def cmd_tasks(message: types.Message, session: AsyncSession):
    user = await get_or_create_user(session, message.from_user.id, message.from_user.username)
    tasks = await get_tasks(session, user.id)

    if not tasks:
        await message.answer("📭 У вас нет задач")
        return

    text = "📋 Ваши задачи:\n\n"
    for i, task in enumerate(tasks, 1):
        status = "✅" if task.is_done else "⏳"
        text += f"{i}. {status} {task.title}\n"

    await message.answer(text)


@router.message(Command("done"))
async def cmd_done(message: types.Message, session: AsyncSession):
    try:
        task_num = int(message.text.replace("/done", "").strip())
    except ValueError:
        await message.answer("❌ Укажите номер задачи: /done 1")
        return

    user = await get_or_create_user(session, message.from_user.id, message.from_user.username)
    tasks = await get_tasks(session, user.id)

    if task_num < 1 or task_num > len(tasks):
        await message.answer("❌ Неправильный номер задачи")
        return

    task = tasks[task_num - 1]
    if task.is_done:
        await message.answer(f"⚠️ Задача уже выполнена: {task.title}")
        return

    await mark_task_done(session, user.id, task.id)
    await message.answer(f"✅ Задача выполнена: {task.title}")