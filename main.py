from fastapi import FastAPI
import uvicorn
from myproject.api import adress,category,contact,courier_product,order,product,review,store,store_menu,user,cart,cart_item
from myproject.admin.setup import setup_admin


myproject = FastAPI()
myproject.include_router(user.user_router)
myproject.include_router(category.category_router)
myproject.include_router(contact.contact_router)
myproject.include_router(courier_product.courier_product_router)
myproject.include_router(order.order_router)
myproject.include_router(product.product_router)
myproject.include_router(review.review_router)
myproject.include_router(store.store_router)
myproject.include_router(store_menu.store_menu_router)
myproject.include_router(adress.address_router)
myproject.include_router(cart_item.cart_item_router)
myproject.include_router(cart.cart_router)
setup_admin(myproject)

if __name__ == '__main__':
    uvicorn.run(myproject,host='127.0.0.1',port=8001)


