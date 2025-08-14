from django.urls import path
from . import views
# from .views import InstallPluginWithCADView

urlpatterns = [
    path('', views.index),
    path('list/', views.list_prisms),
    
    path('<str:id>/', views.prism_detail),
    path('<str:id>/compute/', views.compute_prism),
    
    path('<str:id>/cad/', views.prism_cad),
    
    path("api/prisms/install-plugin/", views.install_plugin),
]
