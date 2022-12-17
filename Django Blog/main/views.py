from django.db.models import Count
from .models import Post, Comment, User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


def homePage(request):
    return render(request, "main/home.html", {})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.get(username=username)
        except:
            return render(request, "main/error.html", {"error_message": "Wrong credentials"})

        user_session = authenticate(request, username=username, password=password)

        if user_session is None:
            return render(request, "main/error.html", {"error_message": "Wrong credentials"})
        else:
            login(request, user_session)
            return redirect("home")

    return render(request, "main/login.html", {})


def userLogout(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    register_form = UserCreationForm()

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        new_user = UserCreationForm(request.POST)

        if new_user.is_valid():
            new_user.save()
            return redirect("login")
        else:
            return render(
                request,
                "main/error.html",
                {"error_message": "An error ocurred during user registration"},
            )

    context = {"register_form": register_form}
    return render(request, "main/register.html", context)


@login_required(login_url="login")
def allPostsPage(request):
    all_posts = Post.objects.annotate(number_of_comments=Count("comment")).order_by("created_at")

    context = {"all_posts": all_posts}
    return render(request, "main/all_posts.html", context)


@login_required(login_url="login")
def likePost(request, id):
    user = request.user

    try:
        post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Not found"})

    if user in post.post_likes.all():
        post.post_likes.remove(user)
        return redirect("all-posts")
    else:
        post.post_likes.add(user)
        return redirect("all-posts")


@login_required(login_url="login")
def createPostPage(request):
    post_author = request.user

    if request.method == "POST":
        post_title = request.POST.get("post_title")
        post_content = request.POST.get("post_content")

        new_post = Post.objects.create(
            post_title=post_title, post_content=post_content, post_author=post_author
        )
        new_post.save()
        return redirect("all-posts")

    return render(request, "main/create_post.html", {})


@login_required(login_url="login")
def commentsPage(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Not found"})

    post_comments = post.comment_set.all()
    context = {"post": post, "post_comments": post_comments}
    return render(request, "main/comments.html", context)


@login_required(login_url="login")
def deletePost(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Not found"})

    if post.post_author.username != str(request.user):
        return render(request, "main/error.html", {"error_message": "Unauthorized"})
    else:
        post.delete()
        return redirect("all-posts")


@login_required(login_url="login")
def updatePostPage(request, id):
    try:
        update_post = Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Not found"})

    if update_post.post_author.username != str(request.user):
        return render(request, "main/error.html", {"error_message": "Unauthorized"})

    if request.method == "POST":
        post_title = request.POST.get("post_title")
        post_content = request.POST.get("post_content")
        Post.objects.filter(id=id).update(post_title=post_title, post_content=post_content)
        return redirect("all-posts")

    context = {"update_post": update_post}
    return render(request, "main/update_post.html", context)


@login_required(login_url="login")
def deleteComment(request, id):
    try:
        delete_comment = Comment.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Not found"})

    if delete_comment.commented_by.username != str(request.user):
        return render(request, "main/error.html", {"error_message": "Unauthorized"})

    delete_comment.delete()
    return redirect("all-posts")


@login_required(login_url="login")
def createCommentPage(request, id):
    commented_by = request.user

    try:
        Post.objects.get(id=id)
    except:
        return render(request, "main/error.html", {"error_message": "Not found"})

    if request.method == "POST":
        comment_content = request.POST.get("comment_content")
        created_post = Comment.objects.create(
            comment_content=comment_content, commented_by=commented_by, commented_post_id=id
        )
        created_post.save()
        return redirect("all-posts")

    return render(request, "main/create_comment.html", {})
