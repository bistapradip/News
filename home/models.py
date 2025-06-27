from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
genre = (('Politics', 'Politics'), ('Entertainment', 'Entertainment'), ('Sports', 'Sports'))

class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    category = models.CharField(choices=genre)

    def __str__(self):
        return self.category



class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    content = RichTextField()
    url = models.CharField(unique=True, max_length=70)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post/")

    def __str__(self):
        return self.title
    
class subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribe = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Subscribed' if self.subscribe else 'Not Subscribed'}"
    

