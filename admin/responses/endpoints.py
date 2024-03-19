from . import *


@useradmin.get('/endpoints', response_model=Page[EndPointsModel], dependencies=[Depends(get_current_user)])
async def endpoints_get(session: AsyncSession = Depends(get_session)):
    try:
        my_routes = select(EndPoints)
        logger.info('Routes have been fetched successfully')
        return await paginate(session, my_routes)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.get('/endpoints', response_model=EndPointsModel, dependencies=[Depends(get_current_user)])
async def get_one_endpoint(endpoint_id: int, session: AsyncSession = Depends(get_session)):
    try:
        endpoint = await session.execute(select(EndPoints).where(EndPoints.id == endpoint_id))
        endpoint = endpoint.unique().scalars().first()
        if endpoint:
            logger.info('User  have been fetched successfully')
            return endpoint
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

@useradmin.post('/endpoints', response_model=EndPointsPostModel, dependencies=[Depends(get_current_user)])
async def endpoints_post(my_route: EndPointsPostModel, session: AsyncSession = Depends(get_session)):
    try:
        my_route = EndPoints(**my_route.dict())
        session.add(my_route)
        await session.commit()
        logger.info(f'Path { my_route } have been created successfully')
        print(my_route)
        return my_route
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.patch('/endpoints/{endpoint_id}', response_model=EndPointsPostModel,
                 dependencies=[Depends(get_current_user)])
async def endpoints_patch(endpoint_id: int, my_route: EndPointsPostModel,
                              session: AsyncSession = Depends(get_session)):
    try:
        check_route = await session.execute(select(EndPoints).where(EndPoints.id == endpoint_id))
        check_route = check_route.scalars().unique().first()
        if check_route:
            await session.execute(update(EndPoints).where(EndPoints.id == endpoint_id).values(**my_route.dict()))
            await session.commit()
            logger.info(f'Path {my_route} have been updated successfully')
            return my_route
        return JSONResponse({"detail": "No Such Path"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.delete('/endpoints/{endpoint_id}', response_model=EndPointsPostModel,
                  dependencies=[Depends(get_current_user)])
async def endpoints_delete(endpoint_id: int, session: AsyncSession = Depends(get_session)):
    try:
        my_route = await session.execute(select(EndPoints).where(EndPoints.id == endpoint_id))
        my_route = my_route.unique().scalars().first()
        if my_route:
            await session.execute(delete(EndPoints).where(EndPoints.id == endpoint_id))
            await session.commit()
            logger.info(f'Path {my_route} have been deleted successfully')
            return my_route
        else:
            return JSONResponse({"detail": "Path Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.get('/endpointsdropdown', response_model=List[EndPointsDropModel], dependencies=[Depends(get_current_user)])
async def endpoints_get_dropdown(session: AsyncSession = Depends(get_session)):
    try:
        all_endpoints = await session.execute(select(EndPoints))
        all_endpoints = all_endpoints.unique().scalars().all()
        logger.info('Endpoints  have been fetched successfully')
        return all_endpoints
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()

