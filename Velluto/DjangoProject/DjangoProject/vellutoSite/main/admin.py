from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Chair, Profile, Order

# Inline для профиля — чтобы редактировать профиль прямо в User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'

# Кастомный UserAdmin с добавленным ProfileInline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    # Убираем email из list_display
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile',)

    # Убираем email из формы редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Отменяем регистрацию стандартного User
admin.site.unregister(User)
# Регистрируем наш кастомный UserAdmin
admin.site.register(User, UserAdmin)


@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    search_fields = ('title',)
    list_filter = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chair', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'chair__title')
    readonly_fields = ('total_price',)
    ordering = ('-created_at',)

# Не регистрируем Profile отдельно, т.к. он инлайн у User
# admin.site.register(Profile)
