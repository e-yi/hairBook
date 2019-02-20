from django.urls import path

from .views import *

urlpatterns = [
    path('faceShape/', faceShape),
    path('face/', FaceListView.as_view()),
    path('hairstyle/', HairstyleListView.as_view()),
    path('hair/', HairListView.as_view()),
]
