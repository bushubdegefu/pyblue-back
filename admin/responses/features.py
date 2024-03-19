from . import *


@useradmin.get('/features', response_model=Page[FeatureModelAll], dependencies=[Depends(get_current_user)])
async def feature_get(session: AsyncSession = Depends(get_session)):
    try:
        logger.info('Feature  have been fetched successfully')
        return await paginate(session, select(Feature))
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.get('/feature/{feature_id}', response_model=FeatureModelAll, dependencies=[Depends(get_current_user)])
async def get_one_feature(feature_id: int, session: AsyncSession = Depends(get_session)):
    try:
        feature = await session.execute(select(Feature).where(Feature.id == feature_id).options(joinedload(Feature.end_points)))
        feature = feature.unique().scalars().first()
        if feature:
            logger.info('User  have been fetched successfully')
            return feature
        else:
            logger.info('No User Found  ')
            return JSONResponse({"detail": "User Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        JSONResponse({"detail": str(e)},
                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.post('/features', response_model=FeatureModel, dependencies=[Depends(get_current_user)])
async def feature_post(feature: FeatureModel, session: AsyncSession = Depends(get_session)):
    try:
        feature = Feature(**feature.model_dump())
        session.add(feature)
        await session.commit()
        logger.info(f'Feature {feature} have been created successfully')
        return feature
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.patch('/features', response_model=FeatureModel, dependencies=[Depends(get_current_user)])
async def feature_patch(feature: FeatureModel, session: AsyncSession = Depends(get_session),
                        ):
    try:
        check_feature = await session.execute(select(Feature).where(Feature.id == feature.id))
        check_feature = check_feature.scalars().unique().first()
        if check_feature:
            await session.execute(update(Feature).where(Feature.id == feature.id).values(**feature.model_dump()))
            await session.commit()
            logger.info(f'Feature {feature} have been updated successfully')
            return feature
        return JSONResponse({"detail": "No Such Feature"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.delete('/features/{feature_id}', response_model=FeatureModel, dependencies=[Depends(get_current_user)])
async def feature_delete(feature_id: int, session: AsyncSession = Depends(get_session)):
    try:
        feature = await session.execute(select(Feature).where(Feature.id == feature_id))
        feature = feature.unique().scalars().first()
        if feature:
            await session.execute(delete(Feature).where(Feature.id == feature_id))
            await session.commit()
            logger.info(f'Feature {feature} have been deleted successfully')
            return feature
        return JSONResponse({"detail": "Feature Not Found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.get('/featuresdropdown', response_model=List[FeatureModel], dependencies=[Depends(get_current_user)])
async def feature_get_dropdown(session: AsyncSession = Depends(get_session)):
    try:
        all_features = await session.execute(select(Feature))
        all_features = all_features.unique().scalars().all()
        logger.info('Feature  have been fetched successfully')
        return all_features
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.patch('/featurestate/{feature_id}', response_model=FeatureModel, dependencies=[Depends(get_current_user)])
async def activate_deactivate_feature(feature_id: int, state: bool, session: AsyncSession = Depends(get_session)):
    try:
        feature = await session.execute(select(Feature).where(Feature.id == feature_id))
        feature = feature.scalars().unique().first()
        if feature:
            await session.execute(update(Feature).where(Feature.id == feature_id).values(active=state))
            await session.commit()
            feature = await session.execute(select(Feature).where(Feature.id == feature_id))
            feature = feature.scalars().unique().first()
            return feature
        return JSONResponse({"detail": "No Such user"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.put('/featuresend/{feature_id}', response_model=FeatureModel, dependencies=[Depends(get_current_user)])
async def add_feature_endpoint(feature_id: int, endpoint_id: int, session: AsyncSession = Depends(get_session)):
    try:
        check_feature = await session.execute(select(Feature).where(Feature.id == feature_id))
        check_feature = check_feature.scalars().unique().first()
        if check_feature:
            await session.execute(update(EndPoints).where(EndPoints.id == endpoint_id).values(feature_id=feature_id))
            await session.commit()
            logger.info(
                f'Feature {check_feature} have been updated successfully')
            return check_feature
        return JSONResponse({"detail": "No Such Feature"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()


@useradmin.delete('/featuresend/{feature_id}', dependencies=[Depends(get_current_user)])
async def delete_feature_endpoint(endpoint_id: int = None, session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(update(EndPoints).where(EndPoints.id == endpoint_id).values(feature_id=None))
        await session.commit()
        return JSONResponse({"detail": "Endpoint Feature updated"}, status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        return JSONResponse({"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        await session.close()
