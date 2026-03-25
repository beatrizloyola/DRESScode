from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_page, name='login'),
    path('cadastro/', views.signup_page, name='signup'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('adicionar-peca/', views.add_piece_page, name='add_piece'),
    path('minhas-pecas/', views.my_pieces_page, name='my_pieces'),
    path('editar-peca/<int:piece_id>/', views.edit_piece, name='edit_piece'),
    path('excluir-peca/<int:piece_id>/', views.delete_piece, name='delete_piece'),
    path('outfits/add/', views.add_outfit_page, name='add_outfit'),
    path('excluir-outfit/<int:outfit_id>/', views.delete_outfit, name='delete_outfit'),
    path('outfits/edit/<int:outfit_id>/', views.edit_outfit_page, name='edit_outfit'),
    path('conta/', views.my_account, name='my_account'),
]