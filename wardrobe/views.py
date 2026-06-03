from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .models import Piece, Outfit
import json
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.db import models
from django.contrib import messages

def landing_page(request):
    return render(request, 'Landing.html')

def signup_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem. Tente novamente.')
            return render(request, 'SignUp.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'SignUp.html')

        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password,
            first_name=name
        )
        user.save()

        messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
        return redirect('login')

    return render(request, 'SignUp.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'E-mail ou senha incorretos.')
            return render(request, 'Login.html')

    return render(request, 'Login.html')

@login_required(login_url='login')
def dashboard_page(request):
    query = request.GET.get('q') or '' 
    
    outfits = Outfit.objects.filter(user=request.user)

    if query:
        outfits = outfits.filter(
            models.Q(name__icontains=query) | 
            models.Q(tags__icontains=query)
        )

    context = {
        'outfits': outfits,
        'search_query': query,
    }
    return render(request, 'Dashboard.html', context)

def logout_user(request):
    logout(request)
    return redirect('landing')

@login_required(login_url='login') 
def add_piece_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        if image and category:
            Piece.objects.create(
                user=request.user,
                image=image,
                name=name,
                category=category
            )
            return redirect('my_pieces')
        else:
            messages.error(request, 'Por favor, insira a imagem e a categoria.')
            return render(request, 'NewPiece.html')

    return render(request, 'NewPiece.html')

@login_required(login_url='login')
def edit_piece(request, piece_id):
    piece = get_object_or_404(Piece, id=piece_id, user=request.user)
    
    if request.method == 'POST':
        piece.name = request.POST.get('name')
        piece.category = request.POST.get('category')
        
        if 'image' in request.FILES:
            piece.image = request.FILES.get('image')
            
        piece.save()
        return redirect('my_pieces')
        
    return render(request, 'EditPiece.html', {'piece': piece})

@login_required(login_url='login')
def delete_piece(request, piece_id):
    piece = get_object_or_404(Piece, id=piece_id, user=request.user)
    
    if request.method == 'POST':
        piece.delete()
        
    return redirect('my_pieces')

@login_required(login_url='login')
def my_pieces_page(request):
    search_query = request.GET.get('q', '').strip()
    
    pieces = Piece.objects.filter(user=request.user)
    
    if search_query:
        pieces = pieces.filter(name__icontains=search_query)

    context = {
        'shirts': pieces.filter(category='shirt'),
        'pants': pieces.filter(category='pants'),
        'shoes': pieces.filter(category='shoes'),
        'search_query': search_query,
        'total_results': pieces.count(),
    }
    
    return render(request, 'MyPieces.html', context)

@login_required(login_url='login')
def add_outfit_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        tags = request.POST.get('tags', '')
        image_data = request.POST.get('image')

        # Pegando IDs com segurança
        shirt_id = request.POST.get('shirt_id')
        pants_id = request.POST.get('pants_id')
        shoes_id = request.POST.get('shoes_id')

        if name and image_data:
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1].split(';')[0] 
            filename = f'{request.user.username}_outfit_{name}.{ext}'
            data = ContentFile(base64.b64decode(imgstr), name=filename)
            
            # Blindagem: Só salva o ID se ele existir e não for a palavra "null"
            novo_outfit = Outfit(
                user=request.user,
                name=name,
                tags=tags,
                shirt_id=shirt_id if shirt_id and shirt_id != 'null' else None,
                pants_id=pants_id if pants_id and pants_id != 'null' else None,
                shoes_id=shoes_id if shoes_id and shoes_id != 'null' else None
            )
            
            novo_outfit.image.save(filename, data, save=True)
            return JsonResponse({'status': 'success', 'message': 'Outfit salvo com sucesso!'})
        return JsonResponse({'status': 'error', 'message': 'Faltam dados'})

    pieces = Piece.objects.filter(user=request.user)
    
    def serialize_pieces(queryset):
        return [{'id': p.id, 'name': p.name, 'category': p.category, 'image': p.image.url, 'alt': p.name} for p in queryset]
        
    context = {
        'shirts_json': json.dumps(serialize_pieces(pieces.filter(category='shirt'))),
        'pants_json': json.dumps(serialize_pieces(pieces.filter(category='pants'))),
        'shoes_json': json.dumps(serialize_pieces(pieces.filter(category='shoes'))),
    }
    return render(request, 'NewOutfit.html', context)

@login_required(login_url='login')
def delete_outfit(request, outfit_id):
    outfit = get_object_or_404(Outfit, id=outfit_id, user=request.user)
    
    if request.method == 'POST':
        outfit.delete()
        
    return redirect('dashboard')

@login_required(login_url='login')
def edit_outfit_page(request, outfit_id):
    outfit = get_object_or_404(Outfit, id=outfit_id, user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        tags = request.POST.get('tags', '')
        image_data = request.POST.get('image')

        shirt_id = request.POST.get('shirt_id')
        pants_id = request.POST.get('pants_id')
        shoes_id = request.POST.get('shoes_id')

        if name and image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1].split(';')[0]
            filename = f'edit_{outfit.id}.{ext}'
            data = ContentFile(base64.b64decode(imgstr), name=filename)
            
            outfit.name = name
            outfit.tags = tags
            # Blindagem para a edição também
            outfit.shirt_id = shirt_id if shirt_id and shirt_id != 'null' else None
            outfit.pants_id = pants_id if pants_id and pants_id != 'null' else None
            outfit.shoes_id = shoes_id if shoes_id and shoes_id != 'null' else None
            
            outfit.image.save(filename, data, save=True)
            return JsonResponse({'status': 'success', 'message': 'Outfit atualizado com sucesso!'})
        return JsonResponse({'status': 'error', 'message': 'Faltam dados'})

    pieces = Piece.objects.filter(user=request.user)
    
    def serialize_pieces(queryset):
        return [{'id': p.id, 'name': p.name, 'category': p.category, 'image': p.image.url, 'alt': p.name} for p in queryset]
        
    context = {
        'outfit': outfit,
        'shirts_json': json.dumps(serialize_pieces(pieces.filter(category='shirt'))),
        'pants_json': json.dumps(serialize_pieces(pieces.filter(category='pants'))),
        'shoes_json': json.dumps(serialize_pieces(pieces.filter(category='shoes'))),
        'current_tags_json': json.dumps(outfit.get_tags_list()), 
    }
    return render(request, 'EditOutfit.html', context)

@login_required(login_url='login')
def my_account(request):
    user = request.user
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        new_password = request.POST.get('new-password')
        current_password = request.POST.get('current-password')

        # Atualiza dados básicos sempre
        user.first_name = name
        user.username = email
        user.email = email
        user.save()

        # Atualiza senha se fornecida
        if new_password and new_password.strip() != "":
            if not current_password:
                messages.error(request, 'Informe a senha atual para alterá-la.')
                return redirect('my_account')
            if check_password(current_password, user.password):
                user.set_password(new_password)
                user.save()
                # Impede que o usuário seja deslogado ao mudar a senha
                update_session_auth_hash(request, user)
            else:
                messages.error(request, 'A senha atual fornecida está incorreta.')
                return redirect('my_account')

        messages.success(request, 'Suas informações foram atualizadas com sucesso!')
        return redirect('my_account')

    return render(request, 'MyAccount.html')