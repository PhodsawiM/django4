from django.shortcuts import render
from django.views.generic import TemplateView
from .form import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate,logout
from rembg import remove
import os
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.
class Home(TemplateView):
    template_name = 'some.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Prepare user data for JSON serialization
        if user.is_authenticated:
            context['user_data'] = {
                'username': user.username,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
                'is_authenticated': True
            }
        else:
            context['user_data'] = {
                'username': None,
                'profile_picture': None,
                'is_authenticated': False
            }
        
        return context
    
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)  # No need to pass request
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Username: {username}, Password: {password}")  # Debug output

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Log the user in
                print('Login successful')
                return redirect('home')  # Redirect to home
            else:
                print('Invalid credentials')  # Debug for invalid login
    else:
        form = CustomUserLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home') 
class profile(TemplateView):
    template_name = 'profile.html'

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to the login page or another view
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required(login_url='/login/')
def remove_background(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the original image and associate it with the user
            image_instance = form.save(commit=False)
            image_instance.user = request.user  # Associate the image with the logged-in user
            image_instance.save()
            
            # Process the background removal
            input_path = os.path.join(settings.MEDIA_ROOT, str(image_instance.original_image))
            output_path = os.path.join(settings.MEDIA_ROOT, 'results', f'bg_removed_{os.path.basename(input_path)}')
            
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()
                output_data = remove(input_data)
                
                # Save the result image
                with open(output_path, 'wb') as output_file:
                    output_file.write(output_data)
                
                # Update the result_image field
                image_instance.result_image = f'results/bg_removed_{os.path.basename(input_path)}'
                image_instance.save()

            return redirect('image_result', image_id=image_instance.id)
    else:
        form = ImageUploadForm()

    return render(request, 'remoiveBG.html', {'form': form})

@login_required
def image_result(request, image_id):
    image_instance = ImageUpload.objects.get(id=image_id)
    return render(request, 'results.html', {'image': image_instance})
@login_required(login_url='/login/')
def user_images_view(request):
    users = CustomUser.objects.prefetch_related('imageupload_set').all()
    return render(request, 'stock.html', {'users': users})
@login_required(login_url='/login/')
def stock(request):
    images = ImageUpload.objects.filter(user=request.user).exclude(original_image__isnull=True)
    return render(request, 'stock.html', {'key1': images})