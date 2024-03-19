from . import *


@useradmin.get('/roles', response_model=Page[RoleModelMatrix], dependencies=[Depends(get_current_user)])
async def role_get(session: AsyncSession = Depends(get_session)):
    try:
        logger.info('Role  have been fetched successfully')
        return await paginate(session, select(Role))
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.get('/roles/{role_id}', response_model=RoleModelAll, dependencies=[Depends(get_current_user)])
async def get_one_role(role_id: int, session: AsyncSession = Depends(get_session)):
    try:
        role = await session.execute(select(Role).where(Role.id == role_id).options(selectinload(Role.app)))
        role = role.unique().scalars().first()
        print(role)
        if role:
            logger.info('Role  have been fetched successfully')
            return role
        else:
            logger.info('No Role Found  ')
            return JSONResponse({"detail": "Role Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        JSONResponse({"detail": str(e)},
                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.post('/roles', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def role_post(role: RoleModel, session: AsyncSession = Depends(get_session)):
    try:
        role = Role(**role.model_dump())
        session.add(role)
        await session.commit()
        logger.info(f'Role {role} have been created successfully')
        return role
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.patch('/roles', response_model=RoleModelMatrix, dependencies=[Depends(get_current_user)])
async def role_patch(role: RoleModelMatrix, session: AsyncSession = Depends(get_session),
                     ):
    try:
        check_role = await session.execute(select(Role).where(Role.id == role.id))
        check_role = check_role.scalars().unique().first()
        if check_role:
            await session.execute(update(Role).where(Role.id == role.id).values(**role.model_dump()))
            await session.commit()
            logger.info(f'Role {role} have been updated successfully')
            return role
        return JSONResponse({"detail": "No Such Role"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.delete('/roles/{role_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def role_delete(role_id: int, session: AsyncSession = Depends(get_session)):
    try:
        role = await session.execute(select(Role).where(Role.id == role_id))
        role = role.unique().scalars().first()
        if role:
            await session.execute(delete(Role).where(Role.id == role_id))
            await session.execute(delete(UserRoles).where(UserRoles.role_id == role_id))
            await session.commit()
            logger.info(f'Role {role} have been deleted successfully')
            return role
        return JSONResponse({"detail": "Role Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.get('/rolesdropdown', response_model=List[RoleModelMatrix], dependencies=[Depends(get_current_user)])
async def role_get_dropdown(user_id: int = None, session: AsyncSession = Depends(get_session)):
    try:
        all_roles = await session.execute(select(Role))
        all_roles = all_roles.unique().scalars().all()
        if user_id:
            my_roles = await session.execute(select(User).where(User.id == user_id).
                                             options(selectinload(User.roles)))
            my_roles = my_roles.unique().scalars().first()
        else:
            my_roles = all_roles
        logger.info('Role  have been fetched successfully')
        my_roles = [RoleModelMatrix.model_validate(
            x).model_dump() for x in all_roles if x not in my_roles.roles]
        return my_roles
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.patch('/rolestate/{role_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def activate_deactivate_role(role_id: int, state: bool, session: AsyncSession = Depends(get_session)):
    try:
        role = await session.execute(select(Role).where(Role.id == role_id))
        role = role.scalars().unique().first()
        if role:
            await session.execute(update(Role).where(Role.id == role_id).values(active=state))
            await session.commit()
            role = await session.execute(select(Role).where(Role.id == role_id))
            role = role.scalars().unique().first()
            return role
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
