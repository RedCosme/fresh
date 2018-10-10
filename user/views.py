from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password

from user.models import UserModel
from user.forms import UserRegisterForm, UserLoginForm
from user.utils import login_required
from goods.models import GoodsModel
# Create your views here.


# 只接受POST请求
def register_post(request):
    """只接受post请求的注册接口"""
    if request.method == "POST":
        user = UserLoginForm(request.POST)
        # print(user)
        # 验证表单数据
        if not user.is_valid():
        # print(user.errors.get_json_data)
        # # print(user.)
        # # print(vaild)
            return JsonResponse(user.errors.get_json_data(), safe=False)
    user = UserLoginForm()
    return render(request, "user/register_post.html", {"user": user})


def register(request):
    """注册接口"""
    cookie = request.COOKIES
    print(cookie)
    if request.method == "POST":
        # 忽略参数为空的情况
        username = request.POST.get("username", "")
        if not username:
            return JsonResponse({"error": "请输入用户名"})
        password = request.POST.get("password", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")
        email = request.POST.get("email", "")

        # 新建用户
        user = UserModel()
        user.username = username
        # 密码加密后存储
        user.password = make_password(password)
        user.phone = phone
        user.address = address
        user.email = email
        user.save()

        return JsonResponse({"user": "success"})

    return render(request, "user/register.html")
    # return render(request, "test.html")


def login(request):
    """登陆接口"""
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        # 当这个jizhu有值的时候， 就是这个复选框被勾选的时候的值1，没有的话是0
        jizhu = request.POST.get("jizhu", 0)

        # 根据用户名查用户对象
        user = UserModel.objects.filter(username=username)

        # 判断，如果没有查到说明用户名错误， 如果查到判断密码是否正确
        # 密码错误： 返回登陆页面，并且提示密码错误
        if user:
            user = user[0]
            # 检查密码是否正确
            is_password = check_password(password, user.password)
            if not is_password:
                # 密码错误
                return render(request, "user/login.html", {"username": username, "is_password": 1, "is_user": 0})
            else:
                # 密码正确
                # 先生成一个response对象
                next_url = request.COOKIES.get("next_url", "/account/login/")
                response = HttpResponseRedirect(next_url)
                # 记住用户名
                # 设置cookie
                if jizhu != 0:
                    response.set_cookie("username", username)
                else:
                    response.set_cookie("username", "", max_age=-1) # max_age指的是过期时间， 当为-1的时候立即过期
                # 把用户id和username放入session中
                request.session["user_id"] = user.id
                request.session["username"] = username
                return response
            # return render(request, "user/index.html", {"username": user.username})
        else:
            return render(request, "user/login.html", {"username": username, "is_user": 1, "is_password": 0})
    # cookie = request.COOKIES
    # 查看cookie有什么
    # print(cookie)
    return render(request, "user/login.html")


# 退出登陆
def logout(request):
    del request.session["user_id"]
    del request.session["username"]
    return redirect("/account/login")


@login_required
def info(request):
    """用户个人信息"""
    user_id = request.session["user_id"]
    user = UserModel.objects.get(id=user_id)
    user_info = {
        "username": user.username,
        "phone": user.phone,
        "address": user.address
    }
    # 从session中拿到商品id的列表（在商品详情里写入session的）
    goods_id_list = request.session.get(str(user_id), [])
    # 用户最近浏览的商品记录
    goods_list = []
    # 通过便利商品id列表，拿到商品对象组成了一个有序的商品对象列表
    for goods_id in goods_id_list:
        goods_list.append(GoodsModel.objects.get(id=goods_id))

    context = {"user_info": user_info,
               "goods_list": goods_list,
               "title": "用户中心"}
    return render(request, "user/user_center_info.html", context)
