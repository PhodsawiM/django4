from django.views.generic import TemplateView
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('login/', login_view,name='login'),
    path('register/', register_view,name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', logout_view, name='profile'),
    path("stock/", stock, name="stock"),
    path('upload/',remove_background, name='upload_image'),
    path('result/<int:image_id>/',image_result, name='image_result'),
    # path('download/<int:image_id>/', download_image, name='download_image'),
    # path('delete/<int:image_id>/', delete_image, name='delete_image'),
]
