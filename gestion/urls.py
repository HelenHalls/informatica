from django.conf.urls import include, url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.message_list, name='index'),
    url(r'^login/$', views.acceso, name='login'),
    url(r'^logout/$', views.salir, name='logout'),
    url(r'^nuevo-usuario/$', views.nuevo_usuario, name='nuevo_usuario'),
    url(r'^usuarios/$', views.users_list, name='lista_usuarios'),
    url(r'^usuarios/(?P<user_details>\w+)/$', views.user_detail, name='detalle_usuario'),
    url(r'^usuarios/(?P<userr>[a-zA-Z0-9_.-]+)/follow/$', views.follow, name='follow'),
    url(r'^usuarios/(?P<userr>[a-zA-Z0-9_.-]+)/unfollow/$', views.unfollow, name='unfollow'),
    url(r'^usuario/seguidores/$', views.ver_seguidores, name='ver_seguidores'),
    url(r'^usuario/seguidos/$', views.ver_seguidos, name='ver_seguidos'),
    url(r'^usuario/add-message/$', views.new_message, name='nuevo_mensaje'),
    url(r'^usuario/message/(?P<pk>[0-9]+)/$', views.message_detail, name='detalle_mensaje'),
    url(r'^usuario/message/(?P<pk>[0-9]+)/add-coment/$', views.new_coment, name='nuevo_comentario'),
]
