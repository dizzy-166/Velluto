from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Order, Chair

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ('chair', 'quantity', 'total_price', 'status', 'created_at', 'delivery_address', 'phone', 'recipient_name')
    can_delete = False
    show_change_link = True

class UserAdmin(DefaultUserAdmin):
    inlines = DefaultUserAdmin.inlines + (OrderInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fio', 'phone', 'email')

@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chair', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'chair__title')
