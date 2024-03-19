from . import *


@useradmin.get('/')
async def adminindex(request: Request, session: AsyncSession = Depends(get_session)) -> Any:
    data = [RouteResponse(name=x.path,route_path=x.name) for x in request.app.routes if x.path != '/']
    try:
        existing = await session.execute(select(RouteResponse))
        existing = existing.unique().scalars().all()
        existing = [x.route_path for x in existing]
        data = [ x for x in data if x.route_path not in existing]
        session.add_all(data)
        await session.commit()
    except Exception as e:
        print(str(e))
        await session.rollback()
    finally:
        await session.close()
    return JSONResponse({'detail': "Working fine"}, status_code=status.HTTP_200_OK)


@useradmin.get('/dashboard')
async def dashboard_get(session: AsyncSession = Depends(get_session)) -> Any:
    res = await session.execute(select(SinglePage).where(SinglePage.active == True))
    res = res.unique().scalars().all()
    board = [UsersPageModelPost.from_orm(x) for x in res]
    board = {x.app: sorted([[f"/{y.name.replace(' ','_').lower()}", y.name] for y in board if y.app == x.app]) for x in board}
    return JSONResponse(board, status_code=status.HTTP_200_OK)
