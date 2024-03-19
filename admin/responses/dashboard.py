from . import *


@useradmin.get('/dashboardfeat', response_model=dict)
async def dashboardfeat(app_id: int, session: AsyncSession = Depends(get_session)) -> Any:
    try:
        app = await session.execute(select(App).where(App.id == app_id).options(selectinload(App.roles).selectinload(Role.features)))
        app = app.scalars().unique().first() 
        app_features = {
            y.name : [x.name for x in y.features] for y in app.roles
        }
        
        if app_features:
            return app_features
        return JSONResponse({"detail": "App Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
   
@useradmin.get('/dashboardpage', response_model=dict)
async def dashboardpage(app_id: int, session: AsyncSession = Depends(get_session)) -> Any:
    try:
        app = await session.execute(select(App).where(App.id == app_id).options(selectinload(App.roles).selectinload(Role.pages)))
        app = app.scalars().unique().first()
        
        app_features = {
            y.name : [x.name for x in y.pages] for y in app.roles
        }
        
        if app_features:
            return app_features
        return JSONResponse({"detail": "App Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.get('/dashboardend', response_model=dict)
async def dashboardend(app_id: int, session: AsyncSession = Depends(get_session)) -> Any:
    try:
        app = await session.execute(select(App).where(App.id == app_id).options(selectinload(App.roles).
                                                                                selectinload(Role.features).selectinload(Feature.end_points)))
        app = app.scalars().unique().first()
        app_ends = {
            y.name : [x.name for z in y.features for x in z.end_points] for y in app.roles
        }
        
        if app_ends:
            return app_ends
        return JSONResponse({"detail": "App Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()   