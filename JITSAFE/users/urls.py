from django.urls import path

from .views import login_view, get_code_view, register_view, getUserView, addUserView, editUserView, deleteUserView, \
    resetPasswordView, changePasswordView

urlpatterns = [
    path('login',login_view.as_view(),name='login'),
    path('get_code',get_code_view.as_view(),name='get_code'),
    path('register',register_view.as_view(),name='register'),
    path('get/users',getUserView.as_view(),name='get_users'),
    path('add/user',addUserView.as_view(),name='add_user'),
    path('update/user',editUserView.as_view(),name='edit_user'),
    path('delete/user',deleteUserView.as_view(),name='delete_user'),
    path('update/password',resetPasswordView.as_view(),name='reset_password'),
    path('change/password',changePasswordView.as_view(),name='change_password')
]