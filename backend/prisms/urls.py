from django.urls import path
from . import views
from .views import InstallPluginWithCADView

urlpatterns = [
    path('', views.index),
    path('list/', views.list_prisms),
    
    path('<str:id>/', views.prism_detail),
    path('<str:id>/compute/', views.compute_prism),
    
    path('<str:id>/cad/', views.prism_cad),
    
    path("api/install-plugin/", InstallPluginWithCADView.as_view(), name="install_plugin"),
]
