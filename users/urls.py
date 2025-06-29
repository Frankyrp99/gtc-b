from django.urls import path

from users.views import UserList,UpdateUserView, RetriveUpdateUserView, EntidadDirectorView, CreateTokenView,EntidadListCreateView

urlpatterns = [
    path("users/list/", UserList.as_view()),
    path("users/<int:pk>/", UpdateUserView.as_view()),
    path("users/", RetriveUpdateUserView.as_view()),
    path("deleteuser/<int:pk>/", UpdateUserView.as_view()),
     path("entidades/", EntidadListCreateView.as_view(), name='entidad-list'),
    path("entidades/<int:pk>/", EntidadDirectorView.as_view()),
    path("token/", CreateTokenView.as_view()),
    path("token/refresh/", CreateTokenView.as_view()),
]
