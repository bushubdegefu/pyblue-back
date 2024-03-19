from . import *

@useradmin.get('/userroles/{user_Id}', response_model=RoleUserModelAll, dependencies=[Depends(get_current_user)])
async def get_user_roles(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.id == user_id).options(selectinload(User.roles)))
        user = user.scalars().unique().first()
        if user:
            return user
        return JSONResponse({"detail": "User Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.post('/userroles/{user_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def post_user_roles(user_id: int, role_id: AddRole, session: AsyncSession = Depends(get_session)):
    try:
        check_role = await session.execute(select(Role).where(Role.id == role_id.role_id))
        check_role = check_role.scalars().unique().first()
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().unique().first()
        if check_role and user:
            user_id = user.id
            data = UserRoles(user_id=user_id, role_id=role_id.role_id)
            session.add(data)
            role = await session.execute(select(Role).where(Role.id == role_id.role_id))
            role = role.scalars().unique().first()
            await session.commit()
            return role
        return JSONResponse({"detail": "User or Role does not Exist"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.delete('/userroles/{user_id}/{role_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def delete_user_roles(user_id: int, role_id: int, session: AsyncSession = Depends(get_session)):
    try:
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().unique().first()
        user_id = user.id
        await session.execute(delete(UserRoles).where(UserRoles.user_id == user_id)
                              .where(UserRoles.role_id == role_id))
        role = await session.execute(select(Role).where(Role.id == role_id))
        role = role.scalars().unique().first()
        await session.commit()
        logger.info(f"{role.name} has been successfully removed from user")
        return role
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
