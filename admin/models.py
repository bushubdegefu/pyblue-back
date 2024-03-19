import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, DateTime, Column, Integer, Float, String, ForeignKey, UniqueConstraint
# from sqlalchemy.dialects.postgresql import UUID
from main.db import Base


# import enum
# from sqlalchemy import Enum

# class MyEnum(enum.Enum):
#     one = 1
#     two = 2
#     three = 3

# t = Table(
#     'data', MetaData(),
#     Column('value', Enum(MyEnum))
# )

class App(Base):
    __tablename__="apps"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(25), unique=True, nullable=False)
    uuid = Column(String(36), unique=True, default=str(uuid.uuid4()))
    active = Column(Boolean(), nullable=False, default=True)
    description = Column(String(255))
    
    def __str__(self):
        return f"{self.name}"
    
class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    active = Column(Boolean(), nullable=False, default=True)
    app_id = Column(Integer(),ForeignKey("apps.id"),nullable=True)
    users = relationship("User", secondary='user_roles', back_populates="roles", lazy='selectin')
    app = relationship("App",backref="roles", lazy=True)

    
    def __str__(self):
        return f"{self.name}"

class User(Base):
    """ User Model for storing user related details """
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    uuid = Column(String(36), unique=True, default=str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    date_registered = Column(DateTime(timezone=True), default=func.now())
    disabled = Column(Boolean(), default=True)
    roles = relationship('Role', secondary='user_roles', back_populates="users", lazy='selectin')

    def __str__(self):
        return f"{self.email}"
    
class Feature(Base):
    __tablename__="features"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(25), unique=True, nullable=False)
    active = Column(Boolean(), nullable=False, default=True)
    description = Column(String(255))
    role_id = Column(Integer(),ForeignKey("roles.id"),nullable=True)
    end_points = relationship("EndPoints", backref="features",lazy=True)
    role = relationship("Role", backref="features",lazy="selectin")
    
    def __str__(self):
        return f"{self.name}"

class EndPoints(Base):
    __tablename__ = 'end_points'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    route_paths = Column(String(300), unique=True, nullable=False)
    description = Column(String(255))
    method = Column(String(10))
    feature_id = Column(Integer(),ForeignKey("features.id"),nullable=True)

    def __str__(self):
        return f"{self.name}"

    
class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(25), unique=True, nullable=False)
    active = Column(Boolean(), nullable=False, default=True)
    description = Column(String(255))
    roles = relationship("Role", secondary="page_roles", backref="pages", lazy='selectin')
    
    def __str__(self):
        return f"{self.name}"



class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    user_id = Column('user_id', Integer(), ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    role_id = Column('role_id', Integer(), ForeignKey('roles.id', ondelete="CASCADE"), nullable=False)
    UniqueConstraint(user_id, role_id)

    def __str__(self):
        return f"<UserRoles '{self.user_id}-{self.role_id}'>"


class PageRoles(Base):
    __tablename__ = 'page_roles'
    id = Column(Integer(), primary_key=True, autoincrement="auto")
    page_id = Column('page_id', Integer(), ForeignKey('pages.id', ondelete="CASCADE"), nullable=False)
    role_id = Column('role_id', Integer(), ForeignKey('roles.id', ondelete="CASCADE"), nullable=False)
    UniqueConstraint(page_id, role_id)

    def __str__(self):
        return f"PageRoles '{self.page_id}-{self.role_id}'"


class JWTSalt(Base):
    __tablename__ = 'jwt_salts'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    salt_a = Column(String(50), nullable=False)
    salt_b = Column(String(50), nullable=True)
    
    def __str__(self):
        return f"salt_a:- {self.salt_a} \n salt_b:- {self.salt_b}"
