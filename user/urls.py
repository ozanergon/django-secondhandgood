from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name="user_update"),
    path('password/', views.change_password, name="change_password"),
    path('orders/', views.orders, name="orders"),
    path('orderdetail/<int:id>', views.orderdetail, name="orderdetail"),
    path('comments/', views.comments, name="comments"),
    path('deletecomment/<int:id>', views.deletecomment, name="deletecomment"),
    path('products/', views.products, name="products"),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('productedit/<int:id>', views.productedit, name='productedit'),
    path('productdelete/<int:id>', views.productdelete, name='productdelete'),
    path('productaddimage/<int:id>', views.productaddimage, name='productaddimage'),
    #path('addcomment/<int:id>', views.addcomment, name='addcomment')
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
]