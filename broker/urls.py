
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('info/<str:symbol>', views.corpRedirect, name="corpRedirect"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("broker_data", views.broker_data, name="broker_data"),
    path("symbols", views.symbols, name="symbols"),
    path("corpData/<str:symbol>", views.corpData, name="corpData"),
    path("buy", views.buy, name="buy"),
    path("sell", views.sell, name="sell"),
    path("charts", views.charts, name="charts"),
    path("orders", views.orders, name="orders"),
    path("personal_data", views.personal_data, name="personal_data"),
    path("services", views.services, name="services")
]
