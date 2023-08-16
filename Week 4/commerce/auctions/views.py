import os
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.core.files import File
from urllib.request import urlretrieve
from django.http import JsonResponse

from .models import Listing, User, Bid, Comment, Category

from . import form_classes

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def new(request):
    if request.method == 'POST':
        form = form_classes.NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            bid = request.POST["bid"]
            user = User.objects.get(pk=request.user.id)
            url = form.cleaned_data["image"]
            listing = Listing(product=title, price=bid, description=text, image=url, user=user, category=category)
            listing.save()
            return HttpResponseRedirect(reverse('success'))
        else:
            return render(request, 'auctions/new.html', {
                "form": form
            })
    return render(request, 'auctions/new.html', {
        "form": form_classes.NewListingForm()
    })

def listing(request, id):
    watched = False
    listing = Listing.objects.get(pk=id)
    comments = listing.comments.all()
    if request.user.id:
        user = User.objects.get(pk=request.user.id)
        watchlist = user.watchlist.all()
        if listing in watchlist:
            watched = True
    if request.method == 'POST':
        try:
            amount = float(request.POST["amount"])
        except:
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "watched": watched,
            "bid_error": True,
            "comments": comments
            })
        listing = Listing.objects.get(pk=id)
        if listing.price >= amount:
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "watched": watched,
            "bid_val_error": True,
            "comments": comments
            })
        user = User.objects.get(pk=request.user.id)
        bids = listing.bids.all()
        for bid in bids:
            if bid.user == user:
                listing.bids.remove(bid)
                break
        bid = Bid(amount=amount, user=user)
        bid.save()
        listing.bids.add(bid)
        listing.winner = user
        listing.price = amount
        listing.save()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watched": watched,
        "comments": comments
    })

@login_required
def watch(request, id):
    user = User.objects.get(pk=request.user.id)
    user.watchlist.add(id)
    return HttpResponseRedirect(reverse('listing', args=(id,)))

@login_required
def unwatch(request, id):
    user = User.objects.get(pk=request.user.id)
    user.watchlist.remove(id)
    return HttpResponseRedirect(reverse('listing', args=(id,)))

@login_required
def close(request, id):
    listing = Listing.objects.get(pk=id)
    if not listing.winner:
        return HttpResponseRedirect(reverse('listing', args=(id,)))
    listing.closed = True
    listing.save()
    return HttpResponseRedirect(reverse('listing', args=(id,)))

@login_required
def comment(request, id):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        text = request.POST["text"]
        comment = Comment(text=text, user=user)
        comment.save()
        listing = Listing.objects.get(pk=id)
        listing.comments.add(comment)
        return HttpResponseRedirect(reverse('listing', args=(id,)))

@login_required
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watchlist = user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        "watchlist": watchlist
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, id):
    category = Category.objects.get(pk=id)
    listings = category.group.all()
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })

def success(request):
    return render(request, 'auctions/success.html')