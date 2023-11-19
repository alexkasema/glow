from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from . models import Profile, Post, LikePost, FollowersCount

from django.contrib import messages #! for flash messages
from django.http import HttpResponse

from itertools import chain

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed)) #! now instead of sending posts to the view we can send feed_list

    posts = Post.objects.all()

    context = {'user_profile': user_profile, 'posts': feed_list}
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
def profile(request, pk):

    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)

    user_posts = Post.objects.filter(user=pk)
    user_posts_len = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object, 'user_posts': user_posts, 
        'user_posts_len': user_posts_len, 'user_profile': user_profile,
        'button_text': button_text, 'user_followers': user_followers,
        'user_following': user_following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('profile/'+user)
    else:
        return redirect('/')

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

@login_required(login_url='signin')
def like_post(request, id):

    username = request.user.username
    post = Post.objects.get(id=id)

    like_filter = LikePost.objects.filter(post_id=id, username=username).first() #! gets the first instance of post

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('index')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('index')


    return HttpResponse('Liked post')