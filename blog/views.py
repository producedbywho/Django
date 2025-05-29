from django.shortcuts import render, get_object_or_404
from .models import Post, Status
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(status = Status.PUBLISHED).order_by('-publish')
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status = Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'PB'  # or whatever represents 'Published'
            post.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post/create.html', {'form': form})