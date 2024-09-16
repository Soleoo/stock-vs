from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from dotenv import load_dotenv
import requests
from .forms import UserRegistrationForm
import os
import random
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
            
            if 'face_image' in request.FILES:
                image_file = request.FILES['face_image']
                api_url = 'http://localhost:8080/upload'
                with image_file.open('rb') as f:
                    files = {'file': f}
                    payload = {
                        'user_id': random.randint(100000, 999999)
                    }
                    response = requests.post(api_url, files=files, data=payload)
                
                if response.status_code == 200:
                    print("Image successfully sent to API")
                    print('[RESPONSE]', response.json())
                else:
                    print("Failed to send image to API")
                    print("[STATUS CODE]", response.status_code)
                    print("[RESPONSE CONTENT]", response.content)
            
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