from django.urls import path
from . import views

app_name = 'audio'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('uploadaudio/', views.UploadView.as_view(), name='uploadaudio'),
    path('recordaudio/', views.RecordView.as_view(), name='recordaudio'),
]
