from django.db import models
from user.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post}, {self.content}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
