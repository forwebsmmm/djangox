from django.urls import path

from .views import RoutesListView, RouteShowView, RouteCreateView, mapShow

urlpatterns = [
    path('<int:pk>/map/', mapShow, name='map_show'),
    path('<int:pk>/show/', RouteShowView.as_view(), name='route_show'),
    path('new/', RouteCreateView.as_view(), name='route_new'),
    path('', RoutesListView.as_view(), name='home'),
    
]