from django.urls import path

from user.views import register, register_post, login, info, logout
# 命名空间名字
app_name = "user"
urlpatterns = [
    path("register/", register, name="register"),
    path("register_post/", register_post, name="register_post"),
    # 登陆接口
    path("login/", login, name="login"),
    # 用户信息接口
    path("info/", info, name="info"),
    # 退出登陆
    path("logout/", logout, name="logout")
]