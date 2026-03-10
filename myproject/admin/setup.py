from .views import (UserProfileAdmin,AddressAdmin,ContactAdmin,CategoryAdmin,CourierProductAdmin,ProductAdmin,StoreAdmin,
                    OrderAdmin,StoreMenuAdmin,  CartItemAdmin,CartAdmin)
from fastapi import FastAPI
from sqladmin import Admin
from myproject.database.db import engine

def setup_admin(myproject: FastAPI):
    admin = Admin(myproject,engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(AddressAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ContactAdmin)
    admin.add_view(CourierProductAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(StoreMenuAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(CartAdmin)
    admin.add_view(CartItemAdmin)