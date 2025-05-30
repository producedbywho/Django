from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Status
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.utils.text import slugify


def post_list(request):
    posts_list = Post.objects.filter(status=Status.PUBLISHED).order_by('-publish')
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post/list.html', {'page_obj': page_obj})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status=Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.active = True  # Θέτουμε το σχόλιο ως ενεργό
            new_comment.save()
            return redirect(post.get_absolute_url())  # Αποφυγή διπλής υποβολής
    else:
        comment_form = CommentForm()

    comments = post.comments.filter(active=True)

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }

    return render(request, 'blog/post/detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'P'
            if not post.slug:
                post.slug = slugify(post.title)
            post.save()
            # Αποθήκευση tag (αν υπάρχει)
            tag = request.POST.get('tags')
            if tag:
                # taggit
                post.tags.set([tag])
            else:
                post.tags.clear()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post/create.html', {'form': form})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='P')
    sent = False

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'name': request.user.username,
            'email': request.user.email
        }
