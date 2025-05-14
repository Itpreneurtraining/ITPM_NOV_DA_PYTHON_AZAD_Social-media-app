from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Post, LikePost, Profile, Followers
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm  # Import your custom form

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('/login')
        else:
            # If the form is invalid, show errors to the user
            return render(request, 'signup.html', {'form': form})
    else:
        form = RegisterForm()  # Initialize the form on GET request
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'invalid': 'Invalid Credentials'})
    return render(request, 'login.html')

@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    return redirect('/login')

# Upload post
@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        Post.objects.create(
            user=request.user.username,
            image=request.FILES.get('image_upload'),
            caption=request.POST.get('caption')
        )
    return redirect('/')

# Like or Unlike a post
@login_required(login_url='/login')
def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)
        like = LikePost.objects.filter(post_id=id, username=username).first()

        if like:
            like.delete()
            post.no_of_likes -= 1
        else:
            LikePost.objects.create(post_id=id, username=username)
            post.no_of_likes += 1

        post.save()
    return redirect('/#' + str(id))

# Explore posts
@login_required(login_url='/login')
def explore(request):
    posts = Post.objects.all().order_by('-created_at')
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'id_user': request.user.id})
    return render(request, 'explore.html', {'post': posts, 'profile': profile})

# View or edit profile
@login_required(login_url='/login')
def profile(request, id_user):
    user_obj = get_object_or_404(User, username=id_user)
    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=user_obj)
    user_posts = Post.objects.filter(user=id_user).order_by('-created_at')

    is_following = Followers.objects.filter(follower=request.user.username, user=id_user).exists()
    follow_status = 'Unfollow' if is_following else 'Follow'

    if request.user.username == id_user and request.method == 'POST':
        # Handle profile picture update
        if 'image' in request.FILES:
            user_profile.profile_picture = request.FILES['image']
            user_profile.bio = request.POST.get('bio')
            user_profile.location = request.POST.get('location')
            user_profile.save()
        return redirect('/profile/' + id_user)
    
    context = {
        'user_object': user_obj,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_posts.count(),
        'profile': profile,
        'follow_unfollow': follow_status,
        'user_followers': Followers.objects.filter(user=id_user).count(),
        'user_following': Followers.objects.filter(follower=id_user).count(),
    }

    return render(request, 'profile.html', context)

# Delete post
@login_required(login_url='/login')
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('/profile/' + request.user.username)

# Search
@login_required(login_url='/login')
def search_results(request):
    query = request.GET.get('q', '')
    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)
    
    # Get list of users the current user is following
    following_list = Followers.objects.filter(
        follower=request.user.username
    ).values_list('user', flat=True)

    # Get the current user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'search_user.html', {
        'query': query,
        'users': users,
        'posts': posts,
        'following_list': following_list,
        'profile': profile,  # Add this line
        'user': request.user  # Add this line
    })
# View single post
@login_required(login_url='/login/')
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Get users not followed by current user (excluding self)
    following = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)
    suggested_users = User.objects.exclude(
        username=request.user.username
    ).exclude(
        username__in=following
    ).order_by('?')[:5]  # Random 5 users

    # Get list of post IDs that the current user has liked
    liked_posts = LikePost.objects.filter(
        username=request.user.username
    ).values_list('post_id', flat=True)
    
    context = {
        'posts': posts,
        'profile': profile,
        'user': request.user,
        'suggested_users': suggested_users,
        'liked_posts': list(liked_posts), 
    }
    return render(request, 'main.html', context)

@login_required(login_url='/login/')
def home_post(request, id):
    post = get_object_or_404(Post, id=id)
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'id_user': request.user.id}
    )
    return render(request, 'main.html', {'posts': [post], 'profile': profile, 'user': request.user})


# Follow/Unfollow
@login_required(login_url='/login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')

        existing = Followers.objects.filter(follower=follower, user=user).first()
        if existing:
            existing.delete()
        else:
            Followers.objects.create(follower=follower, user=user)

        return redirect('/profile/' + user)

    return redirect('/')
