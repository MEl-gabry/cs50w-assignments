from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField


class User(AbstractUser):
    watchlist = ManyToManyField('Listing', blank=True, related_name="watchlist")

class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    product = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="group")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True, blank=True)
    bids = models.ManyToManyField('Bid', blank=True, related_name="bids")
    closed = models.BooleanField(default=False)
    comments = models.ManyToManyField('Comment', blank=True, related_name="comments")

    def __str__(self):
        return f"{self.product}"

class Bid(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", null=True)

    def __str__(self):
        return f"{self.amount} {self.user}"
        

class Comment(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter", null=True)