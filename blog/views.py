from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Category,
    Post,
    Profile,
    Comment,
    PostCreationForm,
    PostEditForm,
    UserLoginForm,
    UserRegistrationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    CommentForm
)
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.generic.list import ListView

def home(requests):
    post_list = Post.published.all().order_by('-id')
    cat_section = Category.objects.all()
    # regional = Post.published.filter(category="regional").order_by('-id')
    # scintific = Post.published.filter(category="scintific").order_by('-id')
    # physics = Post.published.filter(category="physics").order_by('-id')
    # chemistry = Post.published.filter(category="chemistry").order_by('-id')
    # mathematics = Post.published.filter(category="mathematics").order_by('-id')
    # biology = Post.published.filter(category="biology").order_by('-id')
    # sports = Post.published.filter(category="sports").order_by('-id')
    # ai = Post.published.filter(category="ai").order_by('-id')
    # offtopic = Post.published.filter(category="offtopic").order_by('-id')
    # programming = Post.published.filter(category="programming").order_by('-id')
    # datascience = Post.published.filter(category="datascience").order_by('-id')
    # entrance_exam = Post.published.filter(category="entrance_exam").order_by('-id')
    # travel = Post.published.filter(category="travel").order_by('-id')
    # celebrity_talk = Post.published.filter(category="celebrity_talk").order_by('-id')
    # world = Post.published.filter(category="world").order_by('-id')
    # astronomy = Post.published.filter(category="astronomy").order_by('-id')
    # engineering = Post.published.filter(category="engineering").order_by('-id')
    # technology = Post.published.filter(category="technology").order_by('-id')

    query = requests.GET.get("q")

    if query:
        post_list = Post.published.filter(
            Q(title__icontains=query)
            | Q(author__username=query)
            | Q(body__icontains=query)
        )

    paginator = Paginator(post_list, 4)
    page = requests.GET.get("page")
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_page)

    # function called for pagination

    # regional = paginator(regional),
    # scintific = paginator(scintific),
    # physics = paginator(physics),
    # chemistry = paginator(chemistry),
    # mathematics = paginator(mathematics),
    # biology = paginator(post_list),
    # sports = paginator(sports),
    # ai = paginator(ai),
    # offtopic = paginator(offtopic),
    # programming = paginator(programming),
    # datascience = paginator(datascience),
    # entrance_exam = paginator(entrance_exam),
    # travel = paginator(travel),
    # celebrity_talk = paginator(celebrity_talk),
    # world = paginator(world),
    # astronomy = paginator(astronomy),
    # engineering = paginator(engineering),
    # technology = paginator(technology),

    context = {
        "page_obj": page_obj,
        "cat_section": cat_section
        # "regional": regional,
        # "scintific": scintific,
        # "physics" : physics,
        # "chemistry" : chemistry,
        # "mathematics" : mathematics,
        # "biology" : biology,
        # "sports" : sports,
        # "ai" : ai,
        # "offtopic" : offtopic,
        # "programming" : programming,
        # "datascience" : datascience,
        # "entrance_exam" : entrance_exam,
        # "travel" : travel,
        # "celebrity_talk" : celebrity_talk,
        # "world" : world,
        # "astronomy" : astronomy,
        # "engineering" : engineering,
        # "technology" : technology,

    }
    return render(requests, "blog/home.html", context)


def about(requests):
    return render(requests, "blog/about.html")


def post_detail(requests, pk, slug):
    post = get_object_or_404(Post, pk=pk, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False
    if post.likes.filter(id=requests.user.id).exists():
        is_liked = True

    if requests.method == "POST":
        comment_form = CommentForm(requests.POST or None)
        if comment_form.is_valid():
            content = requests.POST.get('content')
            reply_id = requests.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=requests.user, content=content, reply=comment_qs)
            comment.save()
            messages.success(requests, f"Your comment has been posted.")
            # return HttpResponseRedirect(post.get_absolute_url()) 
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "is_liked": is_liked,
        "total_likes": post.total_likes(),
        "comments": comments,
        "comment_form": comment_form
    }
    if requests.is_ajax():
        html = render_to_string("blog/comments.html", context, requests)
        return JsonResponse({"form": html})

    return render(requests, "blog/post_detail.html", context)


def like_post(requests):
    post = get_object_or_404(Post, id=requests.POST.get("id"))
    is_liked = False
    if post.likes.filter(id=requests.user.id).exists():
        post.likes.remove(requests.user)
        is_liked = False
    else:
        post.likes.add(requests.user)
        is_liked = True

    context = {
        "post": post,
        "is_liked": is_liked,
        "total_likes": post.total_likes(),
    }
    if requests.is_ajax():
        html = render_to_string("blog/like_section.html", context, requests)
        return JsonResponse({"form": html})


@login_required
def create_post(requests):
    if requests.method == "POST":
        form = PostCreationForm(requests.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = requests.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(requests, f"Your post has been created!")
            return HttpResponseRedirect(
                reverse("post-detail", args=[post.pk, post.slug])
            )

    else:
        form = PostCreationForm()
    context = {
        "form": form,
    }
    return render(requests, "blog/create_post.html", context)


@login_required
def edit_post(requests, pk):
    post = get_object_or_404(Post, id=pk)
    if post.author != requests.user:
        raise Http404()
    if requests.method == "POST":
        form = PostEditForm(requests.POST or None, instance=post)
        if form.is_valid():
            form.save()
            messages.success(requests, f"Your post has been updated!")
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
    context = {"form": form, "post": post}
    return render(requests, "blog/edit_post.html", context)

@login_required
def delete_post(requests, pk):
    post = get_object_or_404(Post, id=pk)
    # post = Post.objects.get(id=id)
    if post.author != requests.user:
        raise Http404()
    post.delete()
    print(post)
    return redirect('blog-home')

def user_registration(requests):
    if requests.method == "POST":
        form = UserRegistrationForm(requests.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            new_user = form.save()
            Profile.objects.create(user=new_user)
            messages.success(
                requests,
                f"Your account has been created for {username}! Please login now.",
            )
            return redirect("user-login")
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(requests, "blog/user_register.html", context)


def user_login(requests):
    if requests.method == "POST":
        form = UserLoginForm(requests.POST)
        if form.is_valid():
            username = requests.POST["username"]
            password = requests.POST["password"]
            user = authenticate(requests, username=username, password=password)
            if user is not None:
                login(requests, user)
                messages.success(requests, f"You are now loggged in")
                return HttpResponseRedirect(reverse("blog-home"))
    else:
        form = UserLoginForm()

    context = {"form": form}
    return render(requests, "blog/user_login.html", context)


def user_logout(requests):
    logout(requests)
    messages.success(requests, f"You have been loggged out")
    return HttpResponseRedirect(reverse("blog-home"))


@login_required
def profile(requests):
    if requests.method == "POST":
        u_form = UserUpdateForm(requests.POST, instance=requests.user)
        p_form = ProfileUpdateForm(
            requests.POST, instance=requests.user.profile, files=requests.FILES
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(requests, f"Your profile has been updated")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=requests.user)
        p_form = ProfileUpdateForm(instance=requests.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(requests, "user/profile.html", context)


class CatListView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'catlist'
    # paginate_by = 4

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.published.filter(category__name=self.kwargs['category']).filter(status='published'),
            'all': Category.objects.all()
        }
        return content