from django.urls import reverse
from .models import Post, Comment
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


def homePage(request):
    return render(request, "main/home.html", {})


def loginPage(request):
    user = request.user

    if user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        user_session = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user_session is None:
            return render(request, "main/error.html", {"error_message": "Wrong credentials!"})
        else:
            login(request, user_session)
            return redirect("home")

    return render(request, "main/login.html", {})


def userLogout(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    user = request.user
    register_form = UserCreationForm()

    if user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        new_user = UserCreationForm(request.POST)

        if new_user.is_valid():
            new_user.save()
            return redirect("login")
        else:
            return render(request, "main/error.html", {"error_message": new_user.errors})

    return render(request, "main/register.html", {"register_form": register_form})


@login_required(login_url="login")
def allPostsPage(request):
    all_posts = Post.objects.all().order_by("created_at")

    for post in all_posts:
        post.liked_by = post.post_likes.all()
        post.likes_count = post.post_likes.count()
        post.comments_count = post.comment_set.all().count()

    return render(request, "main/all_posts.html", {"all_posts": all_posts})


@login_required(login_url="login")
def likePost(request, id):
    user = request.user

    try:
        post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Post not found!"})

    if user in post.post_likes.all():
        post.post_likes.remove(user)
        return redirect("all-posts")
    else:
        post.post_likes.add(user)
        return redirect("all-posts")


@login_required(login_url="login")
def createPostPage(request):
    user = request.user

    if request.method == "POST":
        Post.objects.create(
            post_author=user, post_title=request.POST["post_title"], post_content=request.POST["post_content"]
        )
        return redirect("all-posts")

    return render(request, "main/create_post.html", {})


@login_required(login_url="login")
def commentsPage(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Post not found!"})

    post.post_comments = post.comment_set.all().order_by("-created_at")

    return render(request, "main/comments.html", {"post": post})


@login_required(login_url="login")
def deletePost(request, id):
    user = str(request.user)

    try:
        post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Post not found!"})

    author = post.post_author.username

    if author != user:
        return render(request, "main/error.html", {"error_message": "Unauthorized!"})
    else:
        post.delete()
        return redirect("all-posts")


@login_required(login_url="login")
def updatePostPage(request, id):
    user = str(request.user)

    try:
        post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Post not found!"})

    author = post.post_author.username

    if author != user:
        return render(request, "main/error.html", {"error_message": "Unauthorized!"})

    if request.method == "POST":
        post.post_title = request.POST["post_title"]
        post.post_content = request.POST["post_content"]
        post.save()
        return redirect("all-posts")

    return render(request, "main/update_post.html", {"post": post})


@login_required(login_url="login")
def deleteComment(request, id):
    user = str(request.user)

    try:
        comment = Comment.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Comment not found!"})

    author = comment.commented_by.username

    if author != user:
        return render(request, "main/error.html", {"error_message": "Unauthorized!"})
    else:
        comment.delete()
        return redirect(reverse("comments", args=[comment.commented_post.id]))


@login_required(login_url="login")
def createCommentPage(request, id):
    user = request.user

    try:
        post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Post not found!"})

    if request.method == "POST":
        Comment.objects.create(commented_by=user, commented_post=post, comment_content=request.POST["comment_content"])
        return redirect(reverse("comments", args=[id]))

    return render(request, "main/create_comment.html", {})
