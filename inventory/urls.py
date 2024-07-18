from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_products, name='listar_productos'),
    path('agregar/', views.add_products, name='agregar_producto'),
    path('editar/<int:pk>/', views.edit_products, name='editar_producto'),
    path('eliminar/<int:pk>/', views.delete_products, name='eliminar_producto'),
]
