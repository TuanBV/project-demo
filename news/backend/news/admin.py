from django.contrib import admin
from django.contrib.auth.models import User
from .models import News, UserProfile
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

admin.site.register(News)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
