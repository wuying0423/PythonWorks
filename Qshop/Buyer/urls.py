from django.urls import path,re_path
from Buyer.views import *
urlpatterns = [
    re_path('^$',Index),
    re_path('index/',Index),
    re_path('goodsdetail/(\d+)',GoodsDetail),
    re_path('uregister/',Uregister),
    re_path('login/',Login),
    re_path('loginout/',LoginOut),
    re_path('carjump/(\d+)',CarJump),
    re_path('carlist/',CarList),
    re_path('clearcar/',ClearCar),
    re_path('orderack/',OrderAck),
    re_path('^ddaddress/',AddAddress),
    re_path('^address/',Address),
    re_path('^changeadd/(\d+)',ChangeAdd),
    re_path('^deladd/(\d+)',DelAdd),

]
