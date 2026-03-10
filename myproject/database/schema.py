from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

from .models import RoleChoices, StatusChoices, CourierStatusChoices


class UserprofileInputSchema(BaseModel):
    phono_number: Optional[str]
    role: RoleChoices
    password: str
    avatar: Optional[str]
    email: EmailStr


class UserprofileOutSchema(BaseModel):
    id: int
    phono_number: Optional[str]
    role: RoleChoices
    avatar: Optional[str]
    email: EmailStr
    data_registered: datetime

class CartInputSchema(BaseModel):
    user_id:int

class CartOutSchema(BaseModel):
    id: int
    user_id: int


class CategoryInputSchema(BaseModel):
    category_name: str


class CategoryOutSchema(BaseModel):
    id: int
    category_name: str


class StoreInputSchema(BaseModel):
    category_id: int
    store_name: str
    description: Optional[str]
    store_image: Optional[str]
    owner_id: int


class StoreOutSchema(BaseModel):
    id: int
    category_id: int
    store_name: str
    description: Optional[str]
    store_image: Optional[str]
    owner_id: int
    cerated_date: date


class ContactInputSchema(BaseModel):
    store_id: int
    contact_number: str


class ContactOutSchema(BaseModel):
    id: int
    store_id: int
    contact_number: str


class AddressInputSchema(BaseModel):
    store_id: int
    address_name: str


class AddressOutSchema(BaseModel):
    id: int
    store_id: int
    address_name: str

class StoreMenuInputSchema(BaseModel):
    store_id: int


class StoreMenuOutSchema(BaseModel):
    id: int
    store_id: int


class ProductInputShema(BaseModel):
    product_name: str
    product_image: str
    product_description: str
    price: int
    quantity: int


class ProductOutShema(BaseModel):
    id: int
    product_name: str
    product_image: str
    product_description: str
    price: int
    quantity: int


class OrderInputSchema(BaseModel):
    product_id: int
    status: StatusChoices
    delivery_address: str
    courier_id: int


class OrderOutSchema(BaseModel):
    id: int
    product_id: int
    status: StatusChoices
    delivery_address: str
    courier_id: int
    created_date: date


class CourierProductInputSchema(BaseModel):
    user_id: int
    order_id: int
    courier_status: CourierStatusChoices


class CourierProductOutSchema(BaseModel):
    id: int
    user_id: int
    order_id: int
    courier_status: CourierStatusChoices

class ReviewInputShema(BaseModel):
    client_id: int
    store_id: int
    courier_id: int
    text: Optional[str]
    rating: int


class ReviewOutShema(BaseModel):
    id: int
    client_id: int
    store_id: int
    courier_id: int
    text: Optional[str]
    rating: int
    created_date: date

class UserLoginShema(BaseModel):
    user_name: str
    password: str

class CartItemInputSchema(BaseModel):
    id:int
    cart_id:int
    product_id:int
    quantity:int

class CartItemOutSchema(BaseModel):
    id:int
    cart_id:int
    product_id:int
    quantity:int


