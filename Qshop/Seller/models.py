from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
# 类型
class Type(models.Model):
    label=models.CharField(max_length=32)
    parent_id=models.IntegerField()
    description=models.CharField(max_length=128)
# 卖家
class Seller(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    photo=models.ImageField(upload_to='img')
    phone=models.CharField(max_length=32)
    address=models.CharField(max_length=32)
    email=models.EmailField(max_length=32)
    id_number=models.CharField(max_length=32)

# 商品
class Goods(models.Model):
    goods_id=models.CharField(max_length=32)
    goods_name=models.CharField(max_length=32)
    goods_price=models.CharField(max_length=32)
    goods_now_price=models.CharField(max_length=32)
    goods_stock=models.CharField(max_length=32)
    goods_description=RichTextUploadingField()
    goods_content=models.TextField()
    goods_show_time=models.DateField()
    goods_status=models.IntegerField(default=0)#商品状态

    type=models.ForeignKey(Type,on_delete=True)
    seller=models.ForeignKey(Seller,on_delete=True)

class Image(models.Model):
    img_address=models.ImageField(upload_to="image")
    img_label=models.CharField(max_length=32)
    img_description=models.TextField()

    goods=models.ForeignKey(Goods,on_delete=True)

class BankCard(models.Model):
    number=models.CharField(max_length=32)
    bankaddr=models.CharField(max_length=32)
    username=models.CharField(max_length=32)
    idCard=models.CharField(max_length=32)
    phone=models.CharField(max_length=32)

    seller=models.ForeignKey(Seller,on_delete=True)