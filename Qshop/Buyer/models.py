from django.db import models
from Seller.models import *
# Create your models here.
# 买家
class Client(models.Model):
    nickname=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    tel=models.CharField(max_length=11)
    password=models.CharField(max_length=32)
    salt=models.CharField(max_length=10)
    activate_status=models.SmallIntegerField(default=0)

#购物车
class shop_car(models.Model):
    goods=models.ForeignKey('Seller.Goods',on_delete=True)
    client=models.ForeignKey('Client',on_delete=True)
    num=models.IntegerField()
    total=models.DecimalField(max_digits=10, decimal_places=2,default=0 )#商品单价
    add_time=models.DateTimeField(auto_now_add=True)

# 收货地址
class client_address(models.Model):
    address=models.CharField(max_length=200)
    contacts=models.CharField(max_length=20)
    tel=models.CharField(max_length=11)
    client=models.ForeignKey('Client',on_delete=True)
    selected=models.BooleanField(default=False)  #设置默认地址

    #     订单
class client_order(models.Model):
    order_code = models.CharField(max_length=32, unique=True)  # 订单编号
    more_order_code = models.CharField(max_length=32)  # 多订单编号 便于订单拆分
    total_money = models.DecimalField(max_digits=10, decimal_places=2)  # 订单总价
    client = models.ForeignKey('Client',on_delete=True)  # 用户买家
    address = models.CharField(max_length=200)  # 发货地址
    contacts = models.CharField(max_length=20)  # 联系方式
    seller = models.ForeignKey('Seller.Seller',on_delete=True)  # 店铺
    tel = models.CharField(max_length=11)  # 电话
    disable = models.SmallIntegerField(default=0)  # 删除时做标记
    add_time = models.DateTimeField(auto_now_add=True)  # 添加时间
    pay_status = models.SmallIntegerField(default=0)  # 支付状态 0：未支付 1：已支付
    pay_time = models.DateTimeField(null=True)  # 支付时间
    pay_money = models.DecimalField(default=0, max_digits=10, decimal_places=2)  # 支付价格

    out_status = models.SmallIntegerField(default=0)  # 发货状态
    in_status = models.SmallIntegerField(default=0)  # 收货支付
    status = models.SmallIntegerField(default=0)  # 已完成

# 商品详情表
class customer_order_info(models.Model):
    order = models.ForeignKey('client_order', on_delete=True)
    goods = models.ForeignKey('Seller.Goods',on_delete=True)
    number = models.SmallIntegerField()
    disable = models.SmallIntegerField(default=0)  # 删除时做标记
    price = models.DecimalField(max_digits=10, decimal_places=2)
    money = models.DecimalField(max_digits=10, decimal_places=2)