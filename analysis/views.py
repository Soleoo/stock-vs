from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from dotenv import load_dotenv
import requests
from .forms import UserRegistrationForm
from django.core.files.base import ContentFile
import base64
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
            user.user_id = random.randint(100000, 999999)
            user.save()
            login(request, user)
            
            send_mail(
                subject = 'Registration Successful',
                message = f'Hello, {user.username},\n\n'
                    'Welcome to Stock-VS! You have been successfully registered.\n\n'
                    'If you have any questions or need assistance, feel free to reach out to our support team.\n\n'
                    'Best regards,\n'
                    'The Stock-VS Team',
                from_email = os.environ.get('EMAIL'),
                recipient_list = [user.email],
                fail_silently = False
            )
            
            if 'face_image' in request.FILES:
                image_file = request.FILES['face_image']
                api_url = os.environ.get('API_ENC_URL')
                with image_file.open('rb') as f:
                    files = {'file': f}
                    payload = {
                        'user_id': user.user_id
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

from django.contrib.auth import get_user_model

def login_view(request):
    if request.method == 'POST':
        if 'face_image' in request.POST and request.POST['face_image']:
            face_image_data = request.POST['face_image']
            format, imgstr = face_image_data.split(';base64,') 
            ext = format.split('/')[-1] 
            image_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            
            api_url = os.environ.get('API_REC_URL')
            with image_file.open('rb') as f:
                files = {'file': f}
                response = requests.post(api_url, files=files)
                if response.status_code == 200:
                    user_id = response.json().get('match')
                    if user_id:
                        User = get_user_model()
                        try:
                            user = User.objects.get(user_id=user_id)
                            login(request, user)
                            return redirect('index')
                        except User.DoesNotExist:
                            return render(request, 'registration/login.html', {'error': 'User not found'})
                else:
                    print("Failed to send image to API")
                    print("[STATUS CODE]", response.status_code)
                    print("[RESPONSE CONTENT]", response.content)
            
            return render(request, 'registration/login.html', {'error': 'Face recognition failed'})
        elif 'email' in request.POST and 'password' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid email or password'})
        else:
            return render(request, 'registration/login.html', {'error': 'No face image provided'})
    
    return render(request, 'registration/login.html')
def profile_view(request):
    return render(request, 'profile.html')