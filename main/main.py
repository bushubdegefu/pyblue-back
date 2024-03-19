import logging
from fastapi import FastAPI, Request
from fastapi_middleware_logger.fastapi_middleware_logger import add_custom_logger
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqladmin import Admin
from main.db import asyncengine
from admin.responses import useradmin
from admin.admin import UserAdmin, RoleAdmin, AppAdmin, PageAdmin
from prometheus_fastapi_instrumentator import Instrumentator
from adminlogging import filehandler


def create_dev_app():
    app = FastAPI(title="fastBlue", version="0.0.1", debug=False)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.addHandler(filehandler)
    app = add_custom_logger(app)
    app.include_router(useradmin, prefix="/useradmin")
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    Instrumentator().instrument(app).expose(app)
    # tok_bear = OAuth2PasswordBearer(tokenUrl="/auth/login")

    admin = Admin(app, asyncengine, title="Privelge Admin Dashboard")

    @app.get("/")
    def index(request: Request):
        print([x.path for x in request.app.routes])
        return {"Message": "Working"}

    add_pagination(app)
    admin.add_view(UserAdmin)
    admin.add_view(RoleAdmin)
    admin.add_view(AppAdmin)
    admin.add_view(PageAdmin)
    return app


def create_testing_app():
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def index():
        return {"Message": "You should make your own index page"}
