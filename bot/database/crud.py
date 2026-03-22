from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User, Task


async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str = None) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def add_task(session: AsyncSession, user_id: int, title: str) -> Task:
    task = Task(user_id=user_id, title=title)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_tasks(session: AsyncSession, user_id: int) -> list[Task]:
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    return result.scalars().all()


async def mark_task_done(session: AsyncSession, user_id: int, task_id: int) -> bool:
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    if task and not task.is_done:
        task.is_done = True
        await session.commit()
        return True
    return False


async def delete_task(session: AsyncSession, user_id: int, task_id: int) -> bool:
    result = await session.execute(
        delete(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    await session.commit()
    return result.rowcount > 0