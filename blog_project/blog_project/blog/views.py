from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import Comment
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth import logout
from django.shortcuts import redirect



def is_admin(user):
    return user.is_staff

def post_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        posts = Post.objects.filter(status='published', title__icontains=search_query)
    else:
        posts = Post.objects.filter(status='published')
    
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    
    if request.method == 'POST':
        if post.status != 'published':
            messages.error(request, 'You cannot comment on unpublished posts.')
            return redirect('blog/post_detail', pk=post.pk)
        
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Your post has been submitted for review.')
            return redirect('my_posts')
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def post_approval_list(request):
    posts = Post.objects.filter(status='draft')
    return render(request, 'blog/post_approval_list.html', {'posts': posts})

@login_required
@user_passes_test(is_admin)
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.status = 'published'
    post.save()
    subject = 'Your post has been approved'
    message = f'Hello {post.author.username},\n\nYour post "{post.title}" has been approved and is now published.\n\nThank you!'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [post.author.email],
        fail_silently=False,
    )
    
    messages.success(request, 'Post has been approved and published.')
    return redirect('post_approval_list')

@login_required
@user_passes_test(is_admin)
def reject_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.status = 'rejected'
    post.save()
    messages.success(request, 'Post has been rejected.')
    return redirect('post_approval_list')

@login_required
@user_passes_test(is_admin)
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, 'Post has been deleted.')
    return redirect('post_approval_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')  
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('post_list')  

def comment_list_or_create(request):
    comments = Comment.objects.all()
    return render(request, 'blog/comment_list.html', {'comments': comments})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def logout_view(request):
    logout(request)
    return redirect('post_list')
