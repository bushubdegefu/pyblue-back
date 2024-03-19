from sqladmin import ModelView
from admin.models import Role, User,Page,App,Feature


class UserAdmin(ModelView, model=User):
    column_list = ['id', 'email', 'password', 'date_registered','roles']
    column_searchable_list = ['email']
    column_default_sort = 'id'
    column_sortable_list = ['id', 'email']
    can_create = True
    form_excluded_columns = [User.date_registered]


class RoleAdmin(ModelView, model=Role):
    column_list = ['id', 'name', 'description']
    column_sortable_list = ['id']
    column_default_sort = 'id'
    can_create = True


class AppAdmin(ModelView, model=App):
    column_list = ['id', 'name', 'uuid', 'description','roles']
    column_searchable_list = ['name', 'description']
    column_default_sort = 'id'
    column_sortable_list = ['id', 'name']
    can_create = True

class PageAdmin(ModelView, model=Page):
    column_list = ['id', 'name','active','description']
    column_searchable_list = ['name',]
    column_default_sort = 'id'
    column_sortable_list = ['id', 'name']
    can_create = True
    

class FeatureAdmin(ModelView, model=Feature):
    column_list = ['id', 'name','active','description','end_points']
    column_searchable_list = ['name',]
    column_default_sort = 'id'
    column_sortable_list = ['id', 'name']
    can_create = True