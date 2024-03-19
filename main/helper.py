
import json
import secrets
from main.db import db_session_sync
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from admin.models import JWTSalt, App, Role, Feature


def update_jwt():
    try:
        jwt_salt = db_session_sync.execute(
            select(JWTSalt).where(JWTSalt.id == 1)).unique().scalars().first()
        print(jwt_salt)
        salt_a = secrets.token_hex(16)
        if jwt_salt.salt_a:
            salt_b = jwt_salt.salt_a
            jwt_salt.salt_a = salt_a
            jwt_salt.salt_b = salt_b
            db_session_sync.commit()
        else:
            salt_b = secrets.token_hex(16)
            new_jwt = JWTSalt(salt_a=salt_a, salt_b=salt_b)
            db_session_sync.add(new_jwt)
            db_session_sync.commit()
    except:
        print('An exception occurred')


def generate_endpoints_json():
    app = db_session_sync.execute(select(App).where(App.id == 1).options(joinedload(App.roles).
                                                                         joinedload(Role.features).joinedload(Feature.end_points)))
    app = app.scalars().unique().first()
    app_ends = {
        y.name: [x.name for z in y.features for x in z.end_points] for y in app.roles
    }
    app_ends = {
        x: key for key, values in app_ends.items() for x in values
    }
    file = open(f"endpoints_role.json", "w")
    json.dump(app_ends, file, indent=0)
    file.close()


def clear_log_files():
    fp = open('blue-logger.log', 'w')
    fp.truncate(0)
    fp.close()
# bluesched.ever
