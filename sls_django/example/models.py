from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.TextField()
    last_used = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
