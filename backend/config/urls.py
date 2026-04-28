from django.contrib import admin
from django.urls import path
from blog import views
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def home(request):
    return HttpResponse("Django API is running")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', views.login),
    path('api/posts', views.posts),
    path('api/create-post', views.create_post),
    path('api/comment/<int:id>', views.comment),
    path('api/update-post/<int:id>', views.update_post),
    path('api/delete-post/<int:id>', views.delete_post),
    path('', home),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]