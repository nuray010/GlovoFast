from sqlalchemy.orm.attributes import backref_listeners

from .db import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,Enum,Date,DateTime,ForeignKey,Text
from enum import Enum as PyEnum
from datetime import date,datetime
from typing import Optional, List

class RoleChoices(str,PyEnum):
    client ='client'
    owner =  'owner'
    courier = 'courier'


class UserProfile(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phono_number: Mapped[str | None] = mapped_column(String, nullable=True, unique=True)
    role:Mapped[RoleChoices] = mapped_column(Enum(RoleChoices),default=RoleChoices.client)
    password: Mapped[str] = mapped_column(String)
    avatar: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    data_registered:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    owner:Mapped[List['Store']] = relationship(back_populates='owner',cascade='all,delete-orphan')
    courier:Mapped[List['Order']] = relationship(back_populates='courier_order',cascade='all,delete-orphan')
    user_courier_product:Mapped[List['CourierProduct']] = relationship(back_populates='user_courier',cascade='all,delete-orphan')
    review_client:Mapped[List['Review']] = relationship(back_populates='client',cascade='all,delete-orphan',  foreign_keys='Review.client_id')
    courier_review:Mapped[List['Review']] = relationship(back_populates='courier',cascade='all,delete-orphan',foreign_keys='Review.courier_id')
    user_token: Mapped[List['RefreshToken']] = relationship("RefreshToken", back_populates='token_user',
                                                            cascade='all,delete-orphan')
    cart_user:Mapped[List['Cart']] = relationship(back_populates='user',cascade='all,delete-orphan')



class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name:Mapped[str] = mapped_column(String(50))
    category:Mapped[List['Store']] = relationship(back_populates='category',cascade='all,delete-orphan')


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id:Mapped[int] = mapped_column(ForeignKey('category.id'))
    category:Mapped[Category] = relationship(back_populates='category')
    store_name:Mapped[str] = mapped_column(String)
    description:Mapped[str | None] = mapped_column(Text,nullable=True)
    store_image:Mapped[str | None] = mapped_column(String,nullable=True)
    owner_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner:Mapped[UserProfile] = relationship(back_populates='owner')
    cerated_date:Mapped[date] = mapped_column(Date,default = date.today())
    store_contact:Mapped[List['Contact']] = relationship(back_populates='store_contact',cascade='all,delete-orphan')
    store_address:Mapped[List['Address']] = relationship(back_populates='store_add',cascade='all,delete-orphan')
    store_menu:Mapped[List['StoreMenu']] = relationship(back_populates='store_menu',cascade='all,delete-orphan')
    review_store:Mapped[List['Review']] = relationship(back_populates='store',cascade='all,delete-orphan')




class Contact(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id:Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_contact:Mapped[Store] = relationship(back_populates='store_contact')
    contact_number:Mapped[str] = mapped_column(String)


class Address(Base):
    __tablename__ = 'addres'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id:Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_add:Mapped[Store] = relationship(back_populates='store_address')
    address_name:Mapped[str] = mapped_column(String)


class StoreMenu(Base):
    __tablename__ = 'store_menu'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id:Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_menu:Mapped[Store] = relationship(back_populates='store_menu')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name:Mapped[str] = mapped_column(String)
    product_image:Mapped[str] = mapped_column(String)
    product_description:Mapped[str] = mapped_column(String)
    price:Mapped[int] = mapped_column(Integer)
    quantity:Mapped[int] = mapped_column(Integer)
    product:Mapped[List['Order']] = relationship(back_populates='product_order',cascade='all,delete-orphan')
    product_cart:Mapped[List['CartItem']] = relationship(back_populates='product',cascade='all,delete-orphan')


class StatusChoices (str, PyEnum):
    pending = 'pending'
    canceled = 'canceled'
    delivered = 'delivered'

class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id:Mapped[int] = mapped_column(ForeignKey('product.id'))
    product_order:Mapped[Product] = relationship(back_populates='product')
    status:Mapped[StatusChoices] = mapped_column(Enum(StatusChoices),default=StatusChoices.pending)
    delivery_address:Mapped[str] = mapped_column(String)
    courier_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    courier_order:Mapped[UserProfile] = relationship(back_populates='courier')
    created_date:Mapped[date] = mapped_column(Date,default=date.today())
    courier_pro:Mapped[List['CourierProduct']] = relationship(back_populates='current_orders',cascade='all,delete-orphan')


class CourierStatusChoices(str,PyEnum):
    busy = 'busy'
    available = 'available'


class CourierProduct(Base):
    __tablename__ = 'courier_product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    user_courier:Mapped[UserProfile] = relationship(back_populates='user_courier_product')
    order_id:Mapped[int] = mapped_column(ForeignKey('order.id'))
    current_orders:Mapped[Order] = relationship(back_populates='courier_pro')
    courier_status:Mapped[CourierStatusChoices] = mapped_column(Enum(CourierStatusChoices),default=CourierStatusChoices.busy)

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    client: Mapped[UserProfile] = relationship(back_populates='review_client', foreign_keys=[client_id])
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped[Store] = relationship(back_populates='review_store')
    courier_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    courier: Mapped[UserProfile] = relationship(back_populates='courier_review', foreign_keys=[courier_id])
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_user: Mapped[UserProfile] = relationship("UserProfile", back_populates='user_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id:  Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    user: Mapped['UserProfile'] = relationship(UserProfile, back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped['Cart'] = relationship(Cart, back_populates='items')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship(back_populates='product_cart')
    quantity: Mapped[int] = mapped_column(Integer, default=1)