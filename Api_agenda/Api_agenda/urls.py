from django.contrib import admin
from django.urls import path
from agenda import views



urlpatterns = [
 path('', views.Home.as_view(), name='index'),
    path('blank/', views.BlankView.as_view(), name='blank'),
    path('cards/', views.CardsView.as_view(), name='cards'),
    path('correos/content/', views.ContentView.as_view(), name='content'),
    path('correos/correo/', views.CorreoView.as_view(), name='correo'),
    path('correos/correo_recuperacion/', views.CorreoRecuperacionView.as_view(), name='correo_recuperacion'),
    path('forms/', views.FormsView.as_view(), name='forms'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('tables/', views.TablesView.as_view(), name='tables'),
    path('userinterface/', views.UserInterfaceView.as_view(), name='userinterface'),
    path('logout/', views.signout, name='logout'),
    path('enviar_correo/<str:correo>/<str:usuario>/<str:contra>/', views.enviar_correo, name='enviar_correo'),
]