from django.urls import path

from users.views import *

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreatelView.as_view()),
    path('<int:pk>/update/', UserUpdatelView.as_view()),
    path('<int:pk>/delete/', UserDeletelView.as_view()),
]
