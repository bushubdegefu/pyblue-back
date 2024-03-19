from . import *


@useradmin.get('/user/{user_id}', response_model=UserModelAll, dependencies=[Depends(get_current_user)])
async def get_one_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.id == user_id).options(joinedload(User.roles)))
        user = user.unique().scalars().first()
        if user:
            logger.info('User  have been fetched successfully')
            return user
        else:
            logger.info('No User Found  ')
            return JSONResponse({"detail": "User Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.get('/user', response_model=Page[UserModelAll], dependencies=[Depends(get_current_user)])
async def get_user(session: AsyncSession = Depends(get_session)):
    try:
        users = select(User).options(joinedload(User.roles)).order_by(User.id)
        return await  paginate(session, users)
    except Exception as e:
        JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.post('/user', response_model=UserModel)
async def post_user(user: UserModelPost, session: AsyncSession = Depends(get_session)):
    try:
        new_user = user.model_dump()
        new_user['password'] = sha512_hash.hash(new_user['password'],salt_size=16)
        print(new_user)
        new_user = User(**new_user)
        new_user.uid = str(uuid.uuid4())
        session.add(new_user)
        await session.commit()
        return new_user
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.patch('/user/{user_id}', response_model=UserModelUpdate, dependencies=[Depends(get_current_user)])
async def patch_user(user_id: int, user: UserModelUpdate, session: AsyncSession = Depends(get_session)):
    try:
        check_user = await session.execute(select(User).where(User.id == user_id))
        check_user = check_user.scalars().unique().first()
        if check_user:
            await session.execute(update(User).where(User.id == user_id).values(**user.dict()))
            await session.commit()
            return user
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.delete('/user/{user_id}', response_model=UserModel, dependencies=[Depends(get_current_user)])
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        check_user = await session.execute(select(User).where(User.id == user_id))
        check_user = check_user.scalars().unique().first()
        user_id = check_user.id
        if check_user:
            await session.execute(delete(User).where(User.id == user_id))
            await session.execute(delete(UserRoles).where(UserRoles.user_id == user_id))
            await session.commit()
            return check_user
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.patch('/activate/{user_id}', response_model=UserModel, dependencies=[Depends(get_current_user)])
async def activate_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().unique().first()
        if user:
            await session.execute(update(User).where(User.id == user_id).values(disabled=False))
            await session.commit()
            user = await session.execute(select(User).where(User.id == user_id))
            user = user.scalars().unique().first()
            return user
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.patch('/deactivate/{user_id}', response_model=UserModel, dependencies=[Depends(get_current_user)])
async def deactivate_user(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().unique().first()
        if user:
            await session.execute(update(User).where(User.id == user_id).values(disabled=True))
            await session.commit()
            user = await session.execute(select(User).where(User.id == user_id))
            user = user.scalars().unique().first()
            return user
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.patch('/password/{user_id}', response_model=UserModel, dependencies=[Depends(get_current_user)])
async def reset_password(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().unique().first()
        if user:
            password = sha512_hash.hash('default@123',salt_size=16)
            await session.execute(update(User).where(User.id == user_id).values(password=password))
            await session.commit()
            user = await session.execute(select(User).where(User.id == user_id))
            user = user.scalars().unique().first()
            return user
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
