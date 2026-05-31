from django.urls import path
from django.contrib.auth import views as auth_views
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

    path('recuperar-senha/', auth_views.PasswordResetView.as_view(
        template_name='PasswordResetForm.html',
        email_template_name='emails/password_reset_email.html',
        subject_template_name='emails/password_reset_subject.txt',
        success_url='/recuperar-senha/enviado/',
    ), name='password_reset'),
    path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='PasswordResetDone.html',
    ), name='password_reset_done'),
    path('recuperar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='PasswordResetConfirm.html',
        success_url='/recuperar-senha/concluido/',
    ), name='password_reset_confirm'),
    path('recuperar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(
        template_name='PasswordResetComplete.html',
    ), name='password_reset_complete'),
]