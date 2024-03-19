import os
import jwt
import uuid
from uuid import uuid4, UUID
from random import randint
from typing import Any, List
from datetime import datetime, timedelta, timezone
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, update, delete, exists, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, subqueryload, selectinload
from passlib.context import CryptContext
from main.db import get_session
from admin.models import User, UserRoles, Role, App, Feature, EndPoints, JWTSalt, Page as SinglePage, PageRoles
from admin.serializers import UserModelAll, UserModelPost, UserModel, UserModelUpdate, LoginUserModel, \
    RoleModel, RoleModelAll, RoleUserModelAll, AddRole, RoleModelMatrix, FeatureModel, FeatureModelAll, AddFeature, \
    EndPointsModel, EndPointsPostModel, EndPointsDropModel, PageModel, PageDropModel, PagePostModel, \
    AppPostModel, AppModel, AppDropModel
from config import settings
from fastapi.security import OAuth2PasswordRequestForm
from admin.responses.oauth import get_current_user, useradmin
from config import settings
from adminlogging import logger
from admin.responses.endpoints import endpoints_get, endpoints_post, endpoints_patch, endpoints_delete, \
    endpoints_get_dropdown, get_one_endpoint
from admin.responses.roles import role_post, role_patch, role_get, role_delete, role_get_dropdown, get_one_role, \
    activate_deactivate_role
from admin.responses.user_roles_operations import get_user_roles, post_user_roles, delete_user_roles
from admin.responses.page_roles_operations import get_page_roles, post_page_roles, delete_page_roles
from admin.responses.login import login_user, login_swagger
from admin.responses.users import get_one_user, get_user, post_user, patch_user, activate_user, \
    deactivate_user, reset_password
from admin.responses.features import feature_get, feature_post, feature_patch, feature_delete, feature_get_dropdown, \
    get_one_feature, activate_deactivate_feature, add_feature_endpoint, delete_feature_endpoint
from admin.responses.pages import pages_get, pages_post, pages_patch, pages_delete, activate_deactivate_page, \
    get_one_page, page_get_dropdown
from admin.responses.apps import apps_get, apps_delete, apps_patch, apps_post, app_get_dropdown, activate_deactivate_app
from admin.responses.dashboard import dashboardpage, dashboardfeat, dashboardend
