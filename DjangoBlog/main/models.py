from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post_content = models.TextField()
    post_title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_likes = models.ManyToManyField(User, default=None, blank=True, related_name="likes")

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_content
