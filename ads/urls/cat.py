from django.urls import path

from ads.views.cat import *

urlpatterns = [
    path('', CategorieListCreateView.as_view()),
    path('<int:pk>', CategorieDetailView.as_view()),
]
