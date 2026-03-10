from myproject.database.models import (
    UserProfile, Address, Category, Contact, CourierProduct, Order,
    Product, Review, Store, StoreMenu, RefreshToken,Cart,CartItem
)
from sqladmin import ModelView

class CartAdmin(ModelView,model=Cart):
    column_list = [Cart.id,Cart.user]

class CartItemAdmin(ModelView,model=CartItem):
    column_list = [CartItem.cart,CartItem.cart_id]

class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.avatar, UserProfile.id, UserProfile.phono_number]


class AddressAdmin(ModelView, model=Address):
    column_list = [Address.address_name, Address.id]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.category_name, Category.category, Category.id]


class ContactAdmin(ModelView, model=Contact):
    column_list = [Contact.contact_number, Contact.id]


class CourierProductAdmin(ModelView, model=CourierProduct):
    column_list = [CourierProduct.user_courier, CourierProduct.courier_status, CourierProduct.id]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.courier_order, Order.id, Order.status]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.product, Product.product_name, Product.product_image]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.client, Review.text, Review.client_id]


class StoreAdmin(ModelView, model=Store):
    column_list = [Store.store_menu, Store.store_name, Store.store_image]


class StoreMenuAdmin(ModelView, model=StoreMenu):
    column_list = [StoreMenu.store_menu, StoreMenu.store_id]