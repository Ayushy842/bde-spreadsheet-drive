from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.upload_file,name="upload-file"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('home/',views.home,name="home"),
    path('all-data/',views.all_Data,name="all-data"),
    path('logout/',views.logout,name="logout"),
]