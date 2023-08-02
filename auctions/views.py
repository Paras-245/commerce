from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listings,Bids,Comments

from .models import User

def index(request):
    activeListings = Listings.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        "activeListings":activeListings
    })


def listingPage(request,listingId):
    usernameByForm = request.user
    listing = Listings.objects.filter(pk=listingId).first()
    isActive = listing.active
    listedByUser = listing.listedByUser
    bid  = listing.bid.all().first()
    bidsMade = bid.noOfBidsMade if bid else 0
    inWatchlist = True if listing.watchlists.filter(username=usernameByForm).first() else False
    winner = listing.winner
    comment = listing.comments.all()

    return render(request,"auctions/listingPage.html",{
        "listing":listing,
        "inWatchlist":inWatchlist,
        "listedByUser":listedByUser,
        "bidsMade":bidsMade,
        "winner":winner,
        "comments":comment,
        "isActive":isActive
    })

def comment(request,listingId):
    listing = Listings.objects.filter(pk=listingId).first()
    commentByForm = request.POST["comment"]
    comment = Comments(**{"comment":commentByForm,"commentedListing":listing,"commentByUser":request.user})
    comment.save()
    return HttpResponseRedirect(reverse("index"))
    

def bidding(request,listingId):
    
    bidByForm = int(request.POST["bidMade"])
    listing = Listings.objects.get(pk=listingId)
    bid  = listing.bid.all().first()
    bidsMade = bid.noOfBidsMade if bid else 0

    if bidsMade > 0:
        if bid.highestBid >= bidByForm or bidByForm < 1:
            return render(request,"auctions/error.html",{
                "messege":"make a higher Bid"
            })
        bid.highestBid = bidByForm
        listing.startingBid = bidByForm
        bid.madeByUser = str(request.user)
        bid.noOfBidsMade += 1
        bid.save()
        listing.save()
    else:
        if listing.startingBid < bidByForm:
            newBid = Bids(**{"highestBid":bidByForm,"noOfBidsMade":1,"listedItem":listing,"madeByUser":request.user})
            listing.startingBid = bidByForm
            newBid.save()
            listing.save()
        else:
            return render(request,"auctions/error.html",{
                "messege":"bid is less than current price"
            })
    return HttpResponseRedirect(reverse("index"))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
def closeListing(request,listingId):
    listing = Listings.objects.get(pk=listingId)
    bid  = listing.bid.all().first()
    bidsMade = bid.noOfBidsMade if bid else 0
    if bidsMade == 0:
        listing.winner = request.user
    else:
        listing.winner = bid.madeByUser
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))
                                
def watchlistManager(request,listingId):
    usernameByForm = request.user
    user = User.objects.get(username=usernameByForm)
    listing = Listings.objects.get(pk=listingId)
    try:
        listing.watchlists.get(username=usernameByForm)
        listing.watchlists.remove(user)
    except:
        listing.watchlists.add(user)
       
    return HttpResponseRedirect(reverse("listingPage",args=(listingId,)))

def watchlist(request):
    usernameByForm = request.user
    user = User.objects.get(username=usernameByForm)
    
    activeListings = user.watchlist.filter(active = True)
    return render(request, "auctions/index.html",{
        "activeListings":activeListings
    })
        

def category(request):
    if request.method == "POST":
        try:
            categoryByForm = request.POST["category"]
        except:
            return render(request,"auctions/error.html",{
                "messege":"category requested not found"
            })
        activeListings = Listings.objects.filter(active=True,category = categoryByForm)
        return render(request, "auctions/index.html",{
            "activeListings":activeListings
        })
    else:
        categories = Listings.objects.order_by().values('category').distinct()
        return render(request,"auctions/category.html",{
            "categories":categories
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


def createListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["startingBid"]
        image = request.POST["image"]
        category = request.POST["category"].lower()
        listedByUser = request.user
        
        listing = Listings(**{"title":title,"description":description,"startingBid":float(startingBid),"image":image,"category":category,"listedByUser":listedByUser})
        listing.save()
        return HttpResponseRedirect(reverse("index"))
        
    else:
        return render(request,"auctions/createListing.html")