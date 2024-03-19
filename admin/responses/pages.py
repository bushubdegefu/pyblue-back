from . import *

@useradmin.get('/pages', response_model=Page[PageModel], dependencies=[Depends(get_current_user)])
async def pages_get(session: AsyncSession = Depends(get_session)):
    try:
        logger.info('Page  have been fetched successfully')
        return await paginate(session, select(SinglePage))
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.get('/pages/{page_id}', response_model=PageModel, dependencies=[Depends(get_current_user)])
async def get_one_page(page_id: int, session: AsyncSession = Depends(get_session)):
    try:
        page = await session.execute(select(SinglePage).where(SinglePage.id == page_id).options(selectinload(SinglePage.roles)))
        page = page.unique().scalars().first()
        if page:
            logger.info('Page  have been fetched successfully')
            return page
        else:
            logger.info('No Page Found  ')
            return JSONResponse({"detail": "Page Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.post('/pages', response_model=PagePostModel, dependencies=[Depends(get_current_user)])
async def pages_post(page: PagePostModel, session: AsyncSession = Depends(get_session)):
    try:
        page = SinglePage(**page.model_dump())
        print(page)
        session.add(page)
        await session.commit()
        logger.info(f'Page {page} have been created successfully')
        return page
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.patch('/pages', response_model=PagePostModel, dependencies=[Depends(get_current_user)])
async def pages_patch(page_id: int, page: PagePostModel, session: AsyncSession = Depends(get_session),
                     ):
    try:
        check_page = await session.execute(select(SinglePage).where(SinglePage.id == page_id))
        check_page = check_page.scalars().unique().first()
        if check_page:
            await session.execute(update(SinglePage).where(SinglePage.id == page_id).values(**page.model_dump()))
            await session.commit()
            logger.info(f'Page {page} have been updated successfully')
            return page
        return JSONResponse({"detail": "No Such Page"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.delete('/pages/{page_id}', response_model=PagePostModel, dependencies=[Depends(get_current_user)])
async def pages_delete(page_id: int, session: AsyncSession = Depends(get_session)):
    try:
        page = await session.execute(select(SinglePage).where(SinglePage.id == page_id))
        page = page.unique().scalars().first()
        if page:
            await session.execute(delete(SinglePage).where(SinglePage.id == page_id))
            # await session.execute(delete(PagePages).where(PagePages.page_id == page_id))
            await session.commit()
            logger.info(f'Page {page} have been deleted successfully')
            return page
        return JSONResponse({"detail": "Page Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.get('/pagesdropdown', response_model=List[PageDropModel], dependencies=[Depends(get_current_user)])
async def page_get_dropdown(session: AsyncSession = Depends(get_session)):
    try:
        all_pages = await session.execute(select(SinglePage))
        all_pages = all_pages.unique().scalars().all()
        logger.info('Page  have been fetched successfully')
        return all_pages
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.patch('/pagestate/{page_id}', response_model=PageModel, dependencies=[Depends(get_current_user)])
async def activate_deactivate_page(page_id: int,state: bool, session: AsyncSession = Depends(get_session)):
    try:
        page = await session.execute(select(SinglePage).where(SinglePage.id == page_id))
        page = page.scalars().unique().first()
        if page:
            await session.execute(update(SinglePage).where(SinglePage.id == page_id).values(active=state))
            await session.commit()
            page = await session.execute(select(SinglePage).where(SinglePage.id == page_id))
            page = page.scalars().unique().first()
            return page
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


