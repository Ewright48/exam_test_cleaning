from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import User, Application

# Главная страница
def home(request):
    return render(request, 'core/home.html')

# Регистрация
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST.get('middle_name', '')
        phone = request.POST['phone']
        email = request.POST['email']
        
        # Проверка пароля
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'core/register.html')
        
        # Проверка длины пароля
        if len(password) < 6:
            messages.error(request, 'Пароль должен быть не менее 6 символов')
            return render(request, 'core/register.html')
        
        # Проверка уникальности
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует')
            return render(request, 'core/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'core/register.html')
        
        # Создание пользователя
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone=phone,
            email=email
        )
        
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно!')
        return redirect('home')
    
    return render(request, 'core/register.html')

# Авторизация
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
    
    return render(request, 'core/login.html')


# Выход
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('login')

# Страница просмотра заявок (история)
@login_required
def applications_view(request):
    user_applications = Application.objects.filter(user=request.user).order_by('-application_date', '-application_time')
    return render(request, 'core/applications.html', {'applications': user_applications})

# Страница создания новой заявки
@login_required
def create_application_view(request):
    if request.method == 'POST':
        address = request.POST['address']
        contact_phone = request.POST['contact_phone']
        application_date = request.POST['application_date']
        application_time = request.POST['application_time']
        service = request.POST['service']
        payment = request.POST['payment']
        
        # Валидация
        from datetime import date, datetime
        today = date.today()
        selected_date = datetime.strptime(application_date, '%Y-%m-%d').date()
        
        if selected_date < today:
            messages.error(request, 'Нельзя выбрать прошедшую дату')
            return render(request, 'core/create_application.html')
        
        if len(contact_phone) < 10:
            messages.error(request, 'Введите корректный номер телефона')
            return render(request, 'core/create_application.html')
        
        if not address.strip():
            messages.error(request, 'Адрес обязателен для заполнения')
            return render(request, 'core/create_application.html')
        
        # Создание заявки
        application = Application.objects.create(
            user=request.user,
            address=address,
            contact_phone=contact_phone,
            application_date=application_date,
            application_time=application_time,
            service=service,
            payment=payment,
            status='new'
        )
        
        messages.success(request, 'Заявка успешно создана! Ожидайте подтверждения администратора.')
        return redirect('applications')
    
    return render(request, 'core/create_application.html')