from django.urls import path
from . import views

app_name = 'text'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('textlize/', views.textlize, name='textlize'),
    path('translatelang/', views.TranslateLang.as_view(), name='translatelang'),
    path('convertfile/', views.ConvertFile.as_view(), name='convertfile'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('media/', views.MediaView.as_view(), name='media'),
    path('audio/', views.AudioView.as_view(), name='audio'),
    path('video/', views.VideoView.as_view(), name='video'),
]
