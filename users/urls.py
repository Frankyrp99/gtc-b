from django.urls import path

from users import views

urlpatterns = [
    path("users/list/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UpdateUserView.as_view()),
    path("users/", views.RetriveUpdateUserView.as_view()),
    path("deleteuser/<int:pk>/", views.UpdateUserView.as_view()),
    path("token/", views.CreateTokenView.as_view()),
    path("token/refresh/", views.CreateTokenView.as_view()),
]
