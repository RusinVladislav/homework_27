from django.urls import path

from ads.views.ad import *

urlpatterns = [
    path('', AdListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreatelView.as_view()),
    path('<int:pk>/update/', AdUpdatelView.as_view()),
    path('<int:pk>/delete/', AdDeletelView.as_view()),
    path('<int:pk>/upload_image', AdUploadImage.as_view()),
]
