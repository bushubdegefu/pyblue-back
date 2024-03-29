from . import *
from .oauth import sha512_hash


@useradmin.post("/login")
async def login_user(login_data: LoginUserModel, session: AsyncSession = Depends(get_session)):
    login_data = login_data.model_dump()
    try:
        if login_data['grant_type'] == 'authorization_code':
            print(login_data)
            user = await session.execute(
                select(User).where(User.email == login_data['email']).options(joinedload(User.roles)))
            user = user.unique().scalars().first()
            data = UserModelAll.model_validate(user).model_dump()
            data['roles'] = [x['name'] for x in data['roles']]
            if sha512_hash.verify(login_data['password'], user.password) and user.password:
                exp = datetime.now(
                    timezone.utc) + timedelta(hours=settings.JWT_APP_TOKEN_EXPIRE_TIME)
                exp2 = datetime.now(
                    timezone.utc) + timedelta(hours=settings.JWT_REFRESH_TOKEN_EXPIRE_TIME)
                key = settings.SECRET_KEY
                del data["password"]
                del data["date_registered"]
                token = jwt.encode(
                    {"data": data, "exp": exp, }, key, algorithm="HS256")
                reftoken = jwt.encode(
                    {'data': data, 'exp': exp2}, key, algorithm="HS256")
                return JSONResponse({"access_token": token, "refresh_token": reftoken, "token_type": "bearer"},
                                    status_code=status.HTTP_202_ACCEPTED)
            return JSONResponse({"detail": "Invalid Password"}, status_code=status.HTTP_401_UNAUTHORIZED)
        elif login_data['grant_type'] == "refresh_token":
            exp = datetime.now(timezone.utc) + timedelta(hours=4)
            exp2 = datetime.now(timezone.utc) + timedelta(hours=5)
            key = settings.SECRET_KEY
            data = jwt.decode(login_data['token'], key, algorithms="HS256")
            data = data["data"]
            token = jwt.encode({'data': data, 'exp': exp},
                               key, algorithm="HS256")
            reftoken = jwt.encode(
                {'data': data, 'exp': exp2}, key, algorithm="HS256")
            return JSONResponse({"access_token": token, "refresh_token": reftoken, "token_type": "bearer"},
                                status_code=status.HTTP_202_ACCEPTED)
        elif login_data['grant_type'] == "token_decode":
            key = settings.SECRET_KEY
            data = jwt.decode(login_data['token'], key, algorithms="HS256")
            return JSONResponse(data["data"], status_code=status.HTTP_206_PARTIAL_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect username or password")
    except Exception as e:
        await session.rollback()
        logger.error(str(e), exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something Unexpected Happened")
    finally:
        await session.close()


@useradmin.post("/token")
async def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    """ This is for swagger UI use only """
    user = await session.execute(
        select(User).where(User.email == form_data.username).options(joinedload(User.roles)))
    user = user.unique().scalars().first()
    data = UserModelAll.model_validate(user).model_dump()
    data['roles'] = [x['name'] for x in data['roles']]
    if sha512_hash.verify(form_data.password, data["password"]):
        exp = datetime.now(timezone.utc) + \
            timedelta(hours=settings.JWT_APP_TOKEN_EXPIRE_TIME)
        exp2 = datetime.now(
            timezone.utc) + timedelta(hours=settings.JWT_REFRESH_TOKEN_EXPIRE_TIME)
        key = settings.SECRET_KEY
        del data["password"]
        del data["date_registered"]
        token = jwt.encode({"data": data, "exp": exp, },
                           key, algorithm="HS256")
        reftoken = jwt.encode({'data': data, 'exp': exp2},
                              key, algorithm="HS256")
        return JSONResponse({"access_token": token, "refresh_token": reftoken, "token_type": "bearer"},
                            status_code=status.HTTP_202_ACCEPTED)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password")
