from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, verbose_name=("username"), on_delete=models.CASCADE)

    def __str__(self):
        return self.title
