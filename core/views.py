# animal_rescue/core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from pets.forms import PetForm
from pets.models import Pet
from .forms import ContactForm 
from django.core.mail import send_mail
from django.conf import settings
import cv2
import numpy as np

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def add_animal(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            image_array = np.fromstring(uploaded_image.read(), np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            species = "Unknown"
            if 'dog' in uploaded_image.name.lower():
                species = "Dog"
            elif 'cat' in uploaded_image.name.lower():
                species = "Cat"
            pet = form.save(commit=False)
            pet.species = species
            pet.save()
            return redirect('pet_list')
    else:
        form = PetForm()

    return render(request, 'core/add_animal.html', {'form': form})

def lost_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            
            
            uploaded_image = request.FILES['image']
            species = "Unknown"
            if 'dog' in uploaded_image.name.lower():
                species = "Dog"
            elif 'cat' in uploaded_image.name.lower():
                species = "Cat"
            pet.species = species

            pet.status = 'lost'
            pet.save()

            
            subject = f'Urgent: New Lost Pet Reported - {pet.name}'
            message = f'A new lost pet has been reported.\n\nName: {pet.name}\nSpecies: {pet.species}\nLocation: {pet.location}\n\nView details: http://127.0.0.1:8000/admin/pets/pet/{pet.id}/'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['admin@yourdomain.com'] 
            
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('pet_list')
    else:
        form = PetForm()
    return render(request, 'core/lost_pet.html', {'form': form})

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            pet.status = new_status
            pet.save()
            return redirect('pet_detail', pet_id=pet.id)

    return render(request, 'core/pet_detail.html', {'pet': pet})

def animal_list(request):
    query = request.GET.get('q')
    species = request.GET.get('species')
    status = request.GET.get('status')

    animals = Pet.objects.all()

    # Filter based on search query (pet name)
    if query:
        animals = animals.filter(name__icontains=query)

    # Filter based on species
    if species:
        animals = animals.filter(species=species)

    # Filter based on status
    if status:
        animals = animals.filter(status=status)
    
    context = {
        'animals': animals,
        'query': query,
        'species': species,
        'status': status,
        'status_choices': Pet.STATUS_CHOICES 
    }
    return render(request, 'core/animal_list.html', context)
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})