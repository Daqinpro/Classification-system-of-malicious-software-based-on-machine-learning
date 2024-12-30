from django.urls import path

from menus.views import get_menus_view, get_menus_list_view, edit_menus_view

urlpatterns= [
    path('get_menus',get_menus_view.as_view(),name='get_menus'),
    path('get/menus',get_menus_list_view.as_view(),name='get_menus_list'),
    path('edit/menu',edit_menus_view.as_view(),name='edit_menu'),

]