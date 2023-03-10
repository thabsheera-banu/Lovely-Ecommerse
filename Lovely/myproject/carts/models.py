from django.db import models
from store.models import Product,Variation
from django.contrib.auth.models import User
# from accounts.models import Account

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return str(self.user)

   

    def sub_total(self):
        return self.product.price * self.quantity


    def __unicode__(self):
        return self.product

class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    is_active=models.BooleanField(default=True)


class Coupen(models.Model):
    code=models.CharField(max_length=50)
    discount=models.IntegerField()
    valid_from=models.DateTimeField()
    valid_to=models.DateTimeField()
    is_active=models.BooleanField()