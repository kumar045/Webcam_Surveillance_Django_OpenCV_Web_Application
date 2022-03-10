from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('products/', views.main, name='products'),
	path('video_feed', views.video_feed, name='video_feed'),
    path('webcam_feed', views.webcam_feed, name='webcam_feed'),
    path('dashboard/camera_control', views.camera_control, name="camera_control"),
    path('main/', views.main, name='main'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/logging_info', views.logging_info, name='logging_info'),
    path('video', views.video, name='video'),
     path('csv_file', views.csv_file, name='csv_file'),

    

]