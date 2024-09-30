from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import UserProfile, User
# from apps.users.forms import CustomUserCreationForm, UpdateProfileForm
from django.contrib.auth.models import Group

from apps.users.custom_forms import CustomSignupForm, CustomUpdateForm

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete=False
    verbose_plural_name="user profile"
    fk_name = 'user'
    view_on_site = True

class CustomUserAdmin(UserAdmin):
    add_form = CustomSignupForm
    form = CustomUpdateForm
    model = User


    list_display_links = ['username']
    search_fields = ['email',]
    ordering = ('-date_joined',)
    inlines = (UserProfileInline,)

    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff',]
    list_filter = ['last_login',]
    fieldsets = (
        (None, {'fields': ['username', 'password']}),
        ('PERSONAL INFO', {'fields': ['first_name', 'last_name', 'email', 'date_of_birth', 'gender'],}),
        ('STATS',  {'fields': ['last_login', 'date_joined'], 'classes': ['collapse']}),
    )
    add_fieldsets = (
        (None, {
            'classes': ["wide","extrapretty"],
            'fields': ['username', 'email','first_name', 'last_name', 'gender', 'date_of_birth', 'password1', 'password2', 'is_staff', 'is_active',]}
         ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
