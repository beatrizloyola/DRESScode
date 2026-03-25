from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Piece

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

def dashboard_page(request):
    return render(request, 'Dashboard.html')

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