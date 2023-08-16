from django.contrib import admin
from .models import Listing, Bid, Category, Comment, User


# Register your models here.

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User)