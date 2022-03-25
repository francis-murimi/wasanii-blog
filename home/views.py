from django.shortcuts import render,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import ExtendedUserCreationForm,ArtistProfileForm,LoginForm,WriterProfileForm
from .models import ArtistProfile,WriterProfile
from shop.models import Art
from blog.models import Blog
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated: 
        username = request.user.username
    else:
        username = 'not logged in'
    context = {'username':username,}
    template = loader.get_template('home/home2.html')
    return HttpResponse(template.render(context,request))


def artist_register(request):
    template = loader.get_template('home/artist_register.html')
    if request.method == 'POST':
        form =ExtendedUserCreationForm(request.POST)
        profile_form = ArtistProfileForm(request.POST)
        
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') 
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
        form = ExtendedUserCreationForm()
        profile_form = ArtistProfileForm()
    
    context = {'form':form,'profile_form':profile_form}
    return HttpResponse(template.render(context,request))

def writer_register(request):
    template = loader.get_template('home/writer_register.html')
    if request.method == 'POST':
        form =ExtendedUserCreationForm(request.POST)
        writer_form = WriterProfileForm(request.POST)
        
        if form.is_valid() and writer_form.is_valid():
            user = form.save()
            age = writer_form.cleaned_data.get('age')
            town = writer_form.cleaned_data.get('town')
            phone = writer_form.cleaned_data.get('phone_number')
            description = writer_form.cleaned_data.get('description')
            WriterProfile.objects.create(user= user,
                                        age = age,
                                        town = town,
                                        phone_number = phone,
                                        description = description)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') 
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
        form = ExtendedUserCreationForm()
        writer_form = WriterProfileForm()
    
    context = {'form':form,'writer_form':writer_form}
    return HttpResponse(template.render(context,request))

def buyer_register(request):
    template = loader.get_template('home/buyer_register.html')
    if request.method == 'POST':
        form =ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') 
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
        form = ExtendedUserCreationForm()
    
    context = {'form':form,}
    return HttpResponse(template.render(context,request))

def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect ('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
    form = LoginForm()
    template = loader.get_template('home/login.html')
    context = {'form':form}
    return HttpResponse(template.render(context,request))

def log_out(request):
    logout(request)
    return redirect('home')

def artist_detail(request,id):
    artist = get_object_or_404(ArtistProfile,id=id)
    a = User.objects.get(username=artist)
    full_name = a.first_name + ' ' + a.last_name
    art = Art.objects.filter(artist=artist)
    template = loader.get_template('home/artist.html')
    context = {'artist':artist,'art':art,'full_name':full_name,'a':a}
    return HttpResponse(template.render(context,request))

def writer_detail(request,id):
    writer = get_object_or_404(WriterProfile,id=id)
    a = User.objects.get(username=writer)
    full_name = a.first_name + ' ' + a.last_name
    blog = Blog.objects.filter(writer = writer)
    template = loader.get_template('home/writer.html')
    context = {'writer':writer,'blog':blog,'full_name':full_name,'a':a}
    return HttpResponse(template.render(context,request))