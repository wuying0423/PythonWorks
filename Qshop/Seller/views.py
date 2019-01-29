import os
import uuid
from Qshop.settings import MEDIA_ROOT,MEDIA_URL
from django.shortcuts import render,HttpResponseRedirect,render_to_response
from django.http import HttpResponse
from Seller.models import *
import hashlib
from django.core.paginator import Paginator
# Create your views here.
# 密码加密
def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result
# 后天注册添加一个用户
# def example(request):
#     s=Seller()
#     s.username = "admin"
#     s.password = setPassword('1111')
#     s.photo = 'img/1.jpg'
#     s.phone = "1232212243"
#     s.address ="北京"
#     s.email = "admin@163.com"
#     s.id_number = "130725200110116666"
#     s.save()
#     return render(request,"seller/base.html")
#
# 校验cookie和session
def cookieCheck(fun):
    def inner(request,*args,**kwargs):
        cookie=request.COOKIES.get("u_name")
        session=request.session.get("u_id")
        user=Seller.objects.filter(username=cookie).first()
        if user and user.id==session:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/seller/login")
    return inner

#登录
def Login(request):
    result={'data':''}
    if request.method=="POST" and request.POST:
        name = request.POST.get('username')
        s_obj = Seller.objects.filter(username=name).first()
        if s_obj:
            passwd = setPassword(request.POST.get('password'))
            if passwd == s_obj.password:
                response =HttpResponseRedirect('/seller/')
                # 设置cookie
                response.set_cookie("u_name",name)
                # 设置session标识
                request.session['u_id']=s_obj.id
                return response
            else:
                result["data"]="用户名或密码错误"
        else:
            result["data"]="用户不存在"
    return render(request,'seller/login.html',{"result":result})

# 退出
def LoginOut(request):
    username=request.COOKIES.get('u_name')
    if username:
        response=HttpResponseRedirect('/seller/login')
        response.delete_cookie("u_name")
        return response
    else:
        return HttpResponseRedirect("/seller/login")

# 显示首页
@cookieCheck
def Index(request):
    return render(request,'seller/index.html')

#商品表列表显示
def GoodsList(request):
    p=request.GET.get('p',1)
    g_obj=Goods.objects.all()
    page=Paginator(g_obj,3)
    goodslist=page.page(p)

    return render(request,'seller/goods_list.html',{'goodslist':goodslist})

# 商品添加
def GoodsAdd(request):
    if request.method=="POST" and request.POST:
        id=int(request.POST.get('type'))

        g_obj=Goods()
        g_obj.goods_id = request.POST.get('goods_id')
        g_obj.goods_name =request.POST.get('goods_name')
        g_obj.goods_price = request.POST.get('goods_price')
        g_obj.goods_now_price = request.POST.get('goods_now_price')
        g_obj.goods_stock = request.POST.get('goods_stock')
        g_obj.goods_description =request.POST.get('goods_description')
        g_obj.goods_content = request.POST.get('goods_content')
        g_obj.goods_show_time =request.POST.get('goods_show_time')
        g_obj.type_id = id
        g_obj.seller_id=int(request.session.get('u_id'))

        g_obj.save()

        files = request.FILES.getlist('img')

        for file in files:
            file_suf = file.name.split(".")[-1]  # 获取文件后缀
            new_file = str(uuid.uuid1()) + '.' + file_suf  # 生成新的文件名 防止重复
            path=os.path.join(MEDIA_ROOT, new_file)
            with open(path, 'wb+') as fb:
                content = file.read()
                fb.write(content)
            file_path = new_file

            img_obj=Image()
            img_obj.img_address = file_path
            img_obj.img_label = g_obj.goods_name
            img_obj.img_description=g_obj.goods_description
            img_obj.goods_id=g_obj.id
            img_obj.save()

        return HttpResponseRedirect('/seller/goodslist')
    else:
        type_obj=Type.objects.all()
        return render(request,'seller/goods_add.html',{"type_obj":type_obj})


def GoodsDetail(request,id):
    id=id
    goods_obj=Goods.objects.filter(id=id).first()
    return render(request,"seller/goods_detail.html",{"goods":goods_obj})



