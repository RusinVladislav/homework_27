from django.urls import path

from ads.views.cat import *

urlpatterns = [
    path('', CategoryListView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),
    path('create/', CategoryCreatelView.as_view()),
    path('<int:pk>/update/', CategoryUpdatelView.as_view()),
    path('<int:pk>/delete/', CategoryDeletelView.as_view()),
]
