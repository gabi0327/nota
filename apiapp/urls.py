from django.urls import path
from . import views
from .views import RegisterUserView




urlpatterns = [
    path('elegir/', views.elegir, name='elegir'),
    path('blog/', views.blog, name='blog'),
    path('blog_registrados/', views.blog_registrados, name='blog_registrados'),
    path('autenticarse/', views.autenticarse, name='autenticarse'),
    path('registarse/', views.registarse, name='registarse'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('guardar_blog/', views.guardar_blog, name='guardar_blog'),
    path('actualizar_blog/<int:blog_id>/', views.actualizar_blog, name='actualizar_blog'),
    path('eliminar_blog/<int:blog_id>/', views.eliminar_blog, name='eliminar_blog'),
    path('mostrar_comentarios/<int:blog_id>/', views.mostrar_comentarios, name='mostrar_comentarios'),
    path('insertar_comentarios/<int:blog_id>/', views.insertar_comentarios, name='insertar_comentarios'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),


]