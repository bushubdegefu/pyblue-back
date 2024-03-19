from . import *

@useradmin.get('/pageroles/{page_Id}', response_model=PageModel, dependencies=[Depends(get_current_user)])
async def get_page_roles(page_id: int, session: AsyncSession = Depends(get_session)):
    try:
        page = await session.execute(select(Page).where(Page.id == page_id).options(selectinload(Page.roles)))
        page = page.scalars().unique().first()
        if page:
            return page
        return JSONResponse({"detail": "Page Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.post('/pageroles/{page_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def post_page_roles(page_id: int, role_id: AddRole, session: AsyncSession = Depends(get_session)):
    try:
        check_role = await session.execute(select(Role).where(Role.id == role_id.role_id))
        check_role = check_role.scalars().unique().first()
        page = await session.execute(select(Page).where(Page.id == page_id))
        page = page.scalars().unique().first()
        if check_role and page:
            page_id = page.id
            data = PageRoles(page_id=page_id, role_id=role_id.role_id)
            session.add(data)
            role = await session.execute(select(Role).where(Role.id == role_id.role_id))
            role = role.scalars().unique().first()
            await session.commit()
            return role
        return JSONResponse({"detail": "Page or Role does not Exist"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.delete('/pageroles/{page_id}/{role_id}', response_model=RoleModel, dependencies=[Depends(get_current_user)])
async def delete_page_roles(page_id: int, role_id: int, session: AsyncSession = Depends(get_session)):
    try:
        page = await session.execute(select(Page).where(Page.id == page_id))
        page = page.scalars().unique().first()
        page_id = page.id
        await session.execute(delete(PageRoles).where(PageRoles.page_id == page_id)
                              .where(PageRoles.role_id == role_id))
        role = await session.execute(select(Role).where(Role.id == role_id))
        role = role.scalars().unique().first()
        await session.commit()
        logger.info(f"{role.name} has been successfully removed from page")
        return role
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
