from . import *

@useradmin.get('/apps', response_model=Page[AppModel], dependencies=[Depends(get_current_user)])
async def apps_get(session: AsyncSession = Depends(get_session)):
    try:
        logger.info('App  have been fetched successfully')
        return await paginate(session, select(App))
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.get('/apps/{app_id}', response_model=AppModel, dependencies=[Depends(get_current_user)])
async def get_one_app(app_id: int, session: AsyncSession = Depends(get_session)):
    try:
        app = await session.execute(select(App).where(App.id == app_id).options(selectinload(App.roles)))
        app = app.unique().scalars().first()
        if app:
            logger.info('App  have been fetched successfully')
            return app
        else:
            logger.info('No App Found  ')
            return JSONResponse({"detail": "App Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.post('/apps', response_model=AppPostModel, dependencies=[Depends(get_current_user)])
async def apps_post(app: AppPostModel, session: AsyncSession = Depends(get_session)):
    try:
        app = App(**app.model_dump())
        print(app)
        session.add(app)
        await session.commit()
        logger.info(f'App {app} have been created successfully')
        return app
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.patch('/apps', response_model=AppPostModel, dependencies=[Depends(get_current_user)])
async def apps_patch(app_id: int, app: AppPostModel, session: AsyncSession = Depends(get_session),
                     ):
    try:
        check_app = await session.execute(select(App).where(App.id == app_id))
        check_app = check_app.scalars().unique().first()
        if check_app:
            await session.execute(update(App).where(App.id == app_id).values(**app.model_dump()))
            await session.commit()
            logger.info(f'App {app} have been updated successfully')
            return app
        return JSONResponse({"detail": "No Such App"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.delete('/apps/{app_id}', response_model=AppPostModel, dependencies=[Depends(get_current_user)])
async def apps_delete(app_id: int, session: AsyncSession = Depends(get_session)):
    try:
        app = await session.execute(select(App).where(App.id == app_id))
        app = app.unique().scalars().first()
        if app:
            await session.execute(delete(App).where(App.id == app_id))
            # await session.execute(delete(AppApps).where(AppApps.app_id == app_id))
            await session.commit()
            logger.info(f'App {app} have been deleted successfully')
            return app
        return JSONResponse({"detail": "App Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.get('/appsdropdown', response_model=List[AppDropModel], dependencies=[Depends(get_current_user)])
async def app_get_dropdown(session: AsyncSession = Depends(get_session)):
    try:
        all_apps = await session.execute(select(App))
        all_apps = all_apps.unique().scalars().all()
        logger.info('App  have been fetched successfully')
        return all_apps
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.patch('/appstate/{app_id}', response_model=AppModel, dependencies=[Depends(get_current_user)])
async def activate_deactivate_app(app_id: int,state: bool, session: AsyncSession = Depends(get_session)):
    try:
        app = await session.execute(select(App).where(App.id == app_id))
        app = app.scalars().unique().first()
        if app:
            await session.execute(update(App).where(App.id == app_id).values(active=state))
            await session.commit()
            app = await session.execute(select(App).where(App.id == app_id))
            app = app.scalars().unique().first()
            return app
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


