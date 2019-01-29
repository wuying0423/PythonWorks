from django.urls import path,re_path
from Seller.views import *
urlpatterns = [

    path('login/',Login,name='login'),
    path('loginout/',LoginOut,name='LoginOut'),

    path('index/',Index),
    re_path('^$',Index),
    path('goodslist/',GoodsList),
    path('goodsadd/',GoodsAdd,name='GoodsAdd'),
    re_path('goodsdetail/(\d+)',GoodsDetail,name='GoodsDetail'),
]
