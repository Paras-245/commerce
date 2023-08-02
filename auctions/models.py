from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    startingBid = models.PositiveIntegerField()
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    listedByUser = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64,default="No one has made a bid",blank=True,null=True)
    watchlists = models.ManyToManyField(User,related_name="watchlist",default=None,blank=True)


    def __str__(self) -> str:
        return f"{self.id} ,{self.title} , {self.startingBid} , {self.image} , {self.date} , {self.listedByUser}"
    class Meta:
        verbose_name_plural = "Listings"

class Bids(models.Model):
    highestBid = models.PositiveIntegerField()
    noOfBidsMade = models.PositiveIntegerField(default=0)
    listedItem = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="bid")
    madeByUser = models.CharField(max_length=64)
    

    class Meta:
        verbose_name_plural = "Bids"

class Comments(models.Model):
    comment = models.TextField(max_length=200)
    commentedListing = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="comments")
    dateOfComment = models.DateTimeField(auto_now_add=True)
    commentByUser = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Comments"

