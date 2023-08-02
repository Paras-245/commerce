from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("createListing", views.createListing, name="createListing"),
    path("listingPage?<str:listingId>", views.listingPage, name="listingPage"),
    path("watchlistManager?<int:listingId>", views.watchlistManager, name="watchlistManager"), 
    path("closeListing?<str:listingId>", views.closeListing, name="closeListing"),
    path("bidding?<str:listingId>", views.bidding, name="bidding"),
    path("comment?<str:listingId>", views.comment, name="comment")
]
