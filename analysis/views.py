from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from dotenv import load_dotenv
from .forms import UserRegistrationForm
import os
load_dotenv()

def index(request):
    return render(request, 'index.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(
                subject='Registration Successful',
                message=f'Hello, {user.username},\n\n'
                    'Welcome to Stock-VS! You have been successfully registered.\n\n'
                    'If you have any questions or need assistance, feel free to reach out to our support team.\n\n'
                    'Best regards,\n'
                    'The Stock-VS Team',
                from_email=os.environ.get('EMAIL'),
                recipient_list=[user.email],
                fail_silently=False
            )
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid email or password'})
    return render(request, 'registration/login.html')

def profile_view(request):
    return render(request, 'profile.html')