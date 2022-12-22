from . import views
from django.urls import path


urlpatterns = [
    path("", views.homePage, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.userLogout, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("all-posts/", views.allPostsPage, name="all-posts"),
    path("like-post/<int:id>", views.likePost, name="like-post"),
    path("create-post/", views.createPostPage, name="create-post"),
    path("comments/<int:id>", views.commentsPage, name="comments"),
    path("delete-post/<int:id>", views.deletePost, name="delete-post"),
    path("update-post/<int:id>", views.updatePostPage, name="update-post"),
    path("delete-comment/<int:id>", views.deleteComment, name="delete-comment"),
    path("create-comment/<int:id>", views.createCommentPage, name="create-comment"),
]
