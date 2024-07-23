from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from exceptions.exceptions import UserAlreadyExists
from api.tasks.models import Task
from api.tasks.schemas import AddTaskSchema, TaskResponseSchema, TaskSchema
from api.users.models import User
from api.users.schemas import UserCreate
from core.security.pwdcrypt import verify_password, password_hasher


async def regisrty_user(
        user_in: UserCreate,
        session: AsyncSession
) -> User:
    hashed_password = password_hasher(user_in.password)
    user_data = user_in.model_dump()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]

    try:
        stmt = insert(User).values(**user_data)
        result = await session.execute(stmt)
        await session.commit()

        # Получение сгенерированного ID
        user_id = result.inserted_primary_key[0]

        # Получение пользователя из базы данных по сгенерированному ID
        user_saved = await session.get(User, user_id)
        return user_saved

    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExists(
            errors=[f"User with id {user_in.username} already exists"])

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def get_user(username: str, session: AsyncSession):
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    try:
        db_dict = result.scalars().all()[0].to_read_model()
    except IndexError:
        return False
    return db_dict


async def get_all_user(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    try:
        db_dict = result.scalars().all()
    except IndexError:
        return False
    return db_dict


async def authenticate_user(
    username: str,
    password: str,
    session: AsyncSession
):
    user: User = await get_user(username, session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_all_tasks_db(session: AsyncSession, user_id: int):
    query = select(Task).where(Task.user_id == user_id)
    result = await session.execute(query)
    result_model = result.scalars().all()
    return result_model


async def get_task_db(session: AsyncSession, task_id: int, user_id: int):
    query = select(Task).where(Task.id == task_id and user_id == user_id)
    result = await session.execute(query)
    try:
        db_dict = result.scalars().all()[0].to_read_model()
    except IndexError:
        return False
    return db_dict


async def update_task_db(session: AsyncSession, task: AddTaskSchema, task_id: int, user_id: int):
    stmt = (
        update(Task)
        .where(Task.id == task_id, Task.user_id == user_id)
        .values(**task.model_dump())
        .returning(Task.id, Task.title, Task.description)
    )
    result = await session.execute(stmt)
    await session.commit()

    updated_task = result.fetchone()

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponseSchema(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description
    )


async def add_task(session: AsyncSession, task: AddTaskSchema, user_id: int):
    new_task = Task(**task.model_dump(), user_id=user_id)
    session.add(new_task)
    await session.commit()
    return TaskSchema.model_validate(new_task)


async def delete_task_db(session: AsyncSession, task_id: int, user_id: int):

    stmt = (
        delete(Task)
        .where(Task.id == task_id, Task.user_id == user_id)
        .returning(Task.id, Task.title, Task.description)
    )
    await session.execute(stmt)
    await session.commit()

    return True
