from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from . models import Profile, Post

from django.contrib import messages #! for flash messages
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()

    context = {'user_profile': user_profile, 'posts': posts}
    return render(request, 'index.html', context)

def signup(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already in use')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #! log in user and redirect to settings page
                user_login = authenticate(request, username=username, password=password)
                login(request, user_login)
                #! create a profile object for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.error(request,'Password mismatch')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'username or password is incorrect')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
@login_required(login_url='signin')
def logoutUser(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):

    user_profile = Profile.objects.get(user=request.user) #! get the currently logged in user

    if request.method == 'POST':

        if request.FILES.get('profile_img') == None:
            image = user_profile.profile_img
            bio = request.POST.get('bio')
            location = request.POST.get('location')

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('profile_img') != None:
            image = request.FILES.get('profile_img')
            bio = request.POST.get('bio')
            location = request.POST.get('location')

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')

    context = {'user_profile': user_profile}
    return render(request, 'setting.html', context)

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('index')
    else:
        return redirect('index')