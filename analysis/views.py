from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from dotenv import load_dotenv
import requests
from .forms import UserRegistrationForm, ProductForm, ProductItemForm
from django.core.files.base import ContentFile
import base64
import os
import random
from .models import Product, ProductItem
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
load_dotenv()

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'welcome.html')

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

def product_list(request):
    products = Product.objects.all()
    return render(request, 'analysis/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'analysis/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            return redirect(reverse('product_list'))
    else:
        form = ProductForm()
    return render(request, 'analysis/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            form.save()
            return redirect(reverse('product_list'))
    else:
        form = ProductForm(instance=product)
    return render(request, 'analysis/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect(reverse('product_list'))
    return render(request, 'analysis/product_confirm_delete.html', {'product': product})

def product_item_list(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    items = ProductItem.objects.filter(product=product)
    return render(request, 'analysis/product_item_list.html', {'product': product, 'items': items})

def product_item_create(request):
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES)
        if form.is_valid():
            product_item = form.save(commit=False)
            qr_code_url = form.cleaned_data.get('qr_code_url')
            if qr_code_url:
                response = requests.get(qr_code_url)
                if response.status_code == 200:
                    qr_code_image = ContentFile(response.content, name='qrcode.png')
                    product_item.qr_code.save('qrcode.png', qr_code_image)
            product_item.save()
            form = ProductItemForm()
            return render(request, 'analysis/product_item_form.html', {'form': form})
    else:
        form = ProductItemForm()
    return render(request, 'analysis/product_item_form.html', {'form': form})
    
def product_item_update(request, pk):
    item = get_object_or_404(ProductItem, pk=pk)
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('product_item_list'))
    else:
        form = ProductItemForm(instance=item)
    return render(request, 'analysis/product_item_form.html', {'form': form})

def product_item_delete(request, serial_number):
    item = get_object_or_404(ProductItem, serial_number=serial_number)
    if request.method == 'POST':
        product_id = item.product.id
        api_url = os.environ.get('API_DELETE_ITEM').replace('{serial_number}', serial_number)
        response = requests.delete(api_url)
        
        if response.status_code == 200:
            item.delete()
            return redirect(reverse('product_item_list', kwargs={'product_id': product_id}))
        else:
            return JsonResponse({'error': 'Failed to delete item via API', 'status_code': response.status_code}, status=response.status_code)
    return render(request, 'analysis/product_item_confirm_delete.html', {'item': item})


def generate_serial_and_qrcode(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    last_item = ProductItem.objects.filter(product=product).order_by('id').last()
    if last_item:
        last_serial = int(last_item.serial_number.split('-')[-1])
        new_serial = f"{product.name[:3].upper()}-{last_serial + 1:03d}"
    else:
        new_serial = f"{product.name[:3].upper()}-001"
    print(new_serial)
    
    qr_code_api_url = os.environ.get('API_QR_GEN_URL')
    qr_code_response = requests.post(qr_code_api_url, json={'serial_number': new_serial})
    print(qr_code_response)
    
    if qr_code_response.status_code == 200:
        qr_code_image_base64 = qr_code_response.json().get('qr_code')
        if qr_code_image_base64:
            qr_code_image = ContentFile(base64.b64decode(qr_code_image_base64), name=f'qrcode_{new_serial}.png')
            
            qr_code_path = default_storage.save(f'qrcodes/qrcode_{new_serial}.png', qr_code_image)
            qr_code_url = request.build_absolute_uri(default_storage.url(qr_code_path))
            
            return JsonResponse({
                'serial_number': new_serial,
                'qr_code_url': qr_code_url
            })
        else:
            return JsonResponse({
                'error': 'QR code image not found in response'
            }, status=500)
    else:
        return JsonResponse({
            'error': 'Failed to generate QR code'
        }, status=500)
        
@csrf_exempt
def scan_qrcode(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        
        objects = ProductItem.objects.filter()
        print(objects)
        
        if image_data:
            api_url = os.environ.get('API_QR_SCAN_URL')
            response = requests.post(api_url, data={'image': image_data})
            if response.status_code == 200:
                product_info = response.json()
                serial_number = product_info['serial_number']
                return JsonResponse({'success': True, 'product_info': serial_number})
            else:
                return JsonResponse({'success': False, 'error': response.status_code})
    return render(request, 'analysis/scan_qrcode.html')

def product_item_detail(request, serial_number):
    item = get_object_or_404(ProductItem, serial_number=serial_number)
    return render(request, 'analysis/product_item_detail.html', {'item': item})

def movements(request):
    return render(request, 'analysis/movements.html')

def reports(request):
    return render(request, 'analysis/reports.html')

def settings(request):
    return render(request, 'analysis/settings.html')