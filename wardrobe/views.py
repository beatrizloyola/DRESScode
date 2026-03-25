from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Piece, Outfit
import json
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse

def landing_page(request):
    return render(request, 'Landing.html')

def signup_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'SignUp.html', {'error': 'As senhas não coincidem. Tente novamente.'})
        
        if User.objects.filter(username=email).exists():
            return render(request, 'SignUp.html', {'error': 'Este e-mail já está cadastrado.'})

        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password,
            first_name=name
        )
        user.save()

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
            return render(request, 'Login.html', {'error': 'E-mail ou senha incorretos.'})

    return render(request, 'Login.html')

@login_required(login_url='login')
def dashboard_page(request):
    search_query = request.GET.get('q', '')
    
    # Pega todos os outfits do usuário logado
    outfits = Outfit.objects.filter(user=request.user)
    
    # Se pesquisou algo, filtra pelo nome
    if search_query:
        outfits = outfits.filter(name__icontains=search_query)
        
    context = {
        'outfits': outfits,
        'search_query': search_query
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
            return render(request, 'NewPiece.html', {'error': 'Por favor, insira a imagem e a categoria.'})

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

# --- AQUI ESTÁ A NOSSA FUNÇÃO CORRIGIDA ---
@login_required(login_url='login')
def my_pieces_page(request):
    search_query = request.GET.get('q', '')
    
    # 1. Pega todas as peças do usuário
    pieces = Piece.objects.filter(user=request.user)
    
    # 2. Se houver algo na pesquisa, filtra as peças pelo nome
    if search_query:
        pieces = pieces.filter(name__icontains=search_query)

    # 3. Divide as peças (agora já filtradas) nas categorias
    context = {
        'shirts': pieces.filter(category='shirt'),
        'pants': pieces.filter(category='pants'),
        'shoes': pieces.filter(category='shoes'),
        'search_query': search_query
    }
    
    return render(request, 'MyPieces.html', context)

@login_required(login_url='login')
def add_outfit_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        tags = request.POST.get('tags', '')
        image_data = request.POST.get('image') # Recebe a imagem em texto (Base64)

        if name and image_data:
            # Converte o texto gerado pelo JavaScript de volta para um arquivo de imagem
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.user.username}_outfit_{name}.{ext}')
            
            # Salva no banco de dados
            Outfit.objects.create(
                user=request.user,
                name=name,
                tags=tags,
                image=data
            )
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Faltam dados'})

    # --- Se for GET (Carregando a página) ---
    pieces = Piece.objects.filter(user=request.user)
    
    # Função auxiliar para transformar as roupas num formato que o JavaScript entende
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
    # Garante que o outfit pertence ao usuário logado antes de deletar
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

        if name and image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'edit_{outfit.id}.{ext}')
            
            # Atualiza o objeto existente
            outfit.name = name
            outfit.tags = tags
            outfit.image = data
            outfit.save()
            return JsonResponse({'status': 'success'})

    # GET: Carrega dados para o editor
    pieces = Piece.objects.filter(user=request.user)
    
    def serialize_pieces(queryset):
        return [{'id': p.id, 'name': p.name, 'category': p.category, 'image': p.image.url, 'alt': p.name} for p in queryset]
        
    context = {
        'outfit': outfit,
        'shirts_json': json.dumps(serialize_pieces(pieces.filter(category='shirt'))),
        'pants_json': json.dumps(serialize_pieces(pieces.filter(category='pants'))),
        'shoes_json': json.dumps(serialize_pieces(pieces.filter(category='shoes'))),
        # Passamos as tags atuais como uma lista simples para o JS
        'current_tags_json': json.dumps(outfit.get_tags_list()), 
    }
    return render(request, 'EditOutfit.html', context)