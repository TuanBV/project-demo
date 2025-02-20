from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import New, UserProfile, Product, Cart, OrderPlaced, Customer
# Register your models here.

# Hiển thị thông tin profile của người dùng trong admin
class UserProfileInline(admin.StackedInline):
    """
    Inline profile for User model
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('birthdate',)

# Thêm UserProfile vào trang admin của User
class CustomUserAdmin(admin.ModelAdmin):
    """
        Custom user profile
    """
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name',)

    # Hide fields
    exclude = ('last_login', )

    def get_birthdate(self, obj):
        """
        Trả về ngày sinh của người dùng
        """
        return obj.userprofile.birthdate if hasattr(obj, 'userprofile') else 'N/A'
    get_birthdate.short_description = 'Birthdate'


# Customize the admin site header and title
admin.site.site_header = 'Website administration'
admin.site.site_title = 'Website administration'
admin.site.index_title = 'Welcome to Website administration'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
@admin.register(New)
class NewModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image_display', 'created_date']

    def image_display(self, obj):
        """
            Return image
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', obj.image.url
            )
        return "No image"
    def created_date(self, obj):
        """
            Return created date
        """
        return obj.published_at.strftime('%Y-%m-%d %H:%M:%S')

    image_display.short_description = 'Image'
    created_date.short_description = 'Created date'


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description',
                    'brand', 'category', 'product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']
