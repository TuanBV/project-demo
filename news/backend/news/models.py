from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
STATE_CHOICES = (
    ('Andaman', 'Andaman'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Daman', 'Daman'),
)

# STATUS
STATUS = (
    ('1', 'Deleted'),
    ('2', 'Hidden'),
    ('3', 'Active'),
    ('4', 'Save')
)


class UserProfile(models.Model):
    """
        Model of user profile
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.user.username

# Create your models here.
class New(models.Model):
    """
        Model of news
    """
    title = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='news_images/', null=True)
    status = models.CharField(choices=STATUS, max_length=10, default='3')
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Customer(models.Model):
    """
        Model of customer
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)
class Product(models.Model):
    """
        Model of product
    """
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product_img/')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    """
        Model of cart
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        """
            Total cost
        """
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    """
        Model of order placed
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_cost(self):
        """
            Total cost
        """
        return self.quantity * self.product.discounted_price
