from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.http import JsonResponse
from Seller.models import *
from Buyer.models import *
import hashlib
# Create your views here.
# def Base(request):
#     return render(request,"buyer/base.html")
def cookieCheck(fun):
    def inner(request,*args,**kwargs):
        cookie=request.COOKIES.get("u_name")
        session=request.session.get("u_id")
        user=Client.objects.filter(nickname=cookie).first()
        if user and user.id==session:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/buyer/login")
    return inner


def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result
# 首页显示
def Index(request):
    goodslist=Goods.objects.all()
    return render(request,'buyer/index.html',{"goodslist":goodslist})

# 买家注册
def Uregister(request):
    result={'data':""}
    if request.method=='POST' and request.POST:
        nickname=request.POST.get('username')
        user=Client.objects.filter(nickname=nickname).first()
        if user:
            result['data']="用户已存在"
            return JsonResponse(result)
        else:
            client=Client()
            client.nickname=nickname
            client.password=setPassword(request.POST.get('password'))
            client.save()
            return render(request,'buyer/users_login.html')
    return render(request,'buyer/users_zhuce.html')

# 用户登录
def Login(request):
    # 或取用户名密码进行比较
    result={"data":""}
    if request.method=="POST" and request.POST:
        user=Client.objects.filter(nickname=request.POST.get("nickname")).first()
        if user:
            passwd=setPassword(request.POST.get("password"))
            if passwd==user.password:
                response= HttpResponseRedirect("/buyer/index/")
                response.set_cookie("u_name",user.nickname)
                request.session["u_id"]=user.id
                return response
            else:
                result["data"]="用户或密码错误"
        else:
            result["data"]="用户不存在"

    return render(request,'buyer/users_login.html',locals())


# 退出
def LoginOut(request):
    username=request.COOKIES.get('u_name')
    if username:
        response=HttpResponseRedirect('/buyer/index')
        response.delete_cookie("u_name")
        del request.session["u_id"]
        return response
    else:
        return HttpResponseRedirect("/buyer/login")

# 商品详情
def GoodsDetail(request,id):

    goods=Goods.objects.filter(id=int(id)).first()
    other=Goods.objects.filter(type_id=goods.type_id)[0:4]
    return render(request,'buyer/goods_details.html',{"goods":goods,'other':other})

# 购物车跳转页
def CarJump(request,id):
    # 显示加入购物车的该商品的详情
    goods=Goods.objects.filter(id=int(id)).first()

    if request.method=="POST" and request.POST:
        u_id=request.session.get("u_id")
        # 实列购物车 加入所选商品 如果购物车中已有 只用改变其数量
        # 没有则加入  还要注意 所对应的用户
        carobj=shop_car.objects.filter(goods_id=int(id),client_id=u_id).first()
        count=request.POST.get('count')
        if carobj:
            carobj.num+=int(count)
            carobj.save()
        else:
            carobj=shop_car()
            carobj.goods_id=goods.id
            carobj.client_id=u_id
            carobj.num=int(count)
            carobj.total=int(count) * float(goods.goods_now_price)
            carobj.save()


        return render(request, 'buyer/car_jump.html', locals())
    else:
        return HttpResponse("404 not found")

# 购物车列表
@cookieCheck
def CarList(request):
    u_id=request.session.get("u_id")
    carlist=shop_car.objects.filter(client_id=u_id)
    total_money=0
    for i in carlist:
        total_money+=i.total
    return render(request,"buyer/cart_list.html",{"carlist":carlist,"total_money":total_money})

# 清空购物车
@cookieCheck
def ClearCar(request):
    u_id=request.GET.get("u_id")
    carlist=shop_car.objects.filter(client_id=u_id)
    carlist.delete()
    return render(request,"buyer/cart_list.html")

# 添加地址信息
@cookieCheck
def AddAddress(request):
    u_id=request.session.get("u_id")
    if request.method=="POST" and request.POST:
        add=client_address()
        add.address=request.POST.get("buyer_address")
        add.contacts=request.POST.get("buyer_contacts")
        add.tel=request.POST.get("buyer_tel")
        add.client_id=u_id
        add.save()

        return render(request,"buyer/address.html")
    return render(request,"buyer/addaddress.html")

# 修改地址信息
@cookieCheck
def ChangeAdd(request,id):
    id=id
    add = client_address.objects.filter(id=id).first()
    if request.method=="POST" and request.POST:

        add.address = request.POST.get("buyer_address")
        add.contacts = request.POST.get("buyer_contacts")
        add.tel = request.POST.get("buyer_tel")
        add.client_id =id
        add.save()
        return HttpResponseRedirect("/buyer/address")

    return render(request,"buyer/addaddress.html",{"addr":add})

# 删除地址信息
@cookieCheck
def DelAdd(request,id):
    id=id
    add=client_address.objects.filter(id=id).first()
    add.delete()
    return HttpResponseRedirect("/buyer/address/")

# 地址信息展示
@cookieCheck
def Address(request):
    u_id=request.session.get("u_id")
    add=client_address.objects.filter(client_id=u_id)
    return render(request,"buyer/address.html",{"address_list":add})

# 订单确认
@cookieCheck
def  OrderAck(request):
    u_id=request.session.get("u_id")
    goodslist=[]
    addlist=client_address.objects.filter(client_id=u_id)
    if request.method=="POST" and request.POST:
        data=request.POST
        money=0
        for key,value in data.items():
            print(key,value)
            if key.startswith("name"):
                buyCar=shop_car.objects.get(id=int(value))
                money+=buyCar.total
                goodslist.append({"buyCar":buyCar})
        return render(request,"buyer/order_ack.html",{"goodslist":goodslist,"addlist":addlist,"money":money})

    return render(request,"buyer/order_ack.html")

# 提交订单
@cookieCheck
def SubOrder(request):
#     提交订单 获取数据
    if request.method=="POST" and request.POST:
        g_list=request.POST.get("refer")
        money=request.POST.get("money")
        # 获取数据 添加到订单表
        order_obj=client_order()
        for goods in g_list:
            
#保存数据
     # 根据店铺拆分订单
     pass


