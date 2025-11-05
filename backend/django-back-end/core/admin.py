from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(DjangoUserAdmin, SimpleHistoryAdmin):
    list_display = ('identifier', 'nome', 'user_type', 'is_active', 'is_staff', 'created_at')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('identifier', 'nome', 'email')
    ordering = ('created_at',)

    fieldsets = (
        (None, {'fields': ('identifier', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'email', 'user_type', 'metadata')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('identifier', 'nome', 'password1', 'password2', 'email', 'user_type')
        })
    )

    def ativar_user(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} User ativado com sucesso.")

    ativar_user.short_description = "Ativar usuários selecionados"

    def desativar_user(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} User ativado com sucesso.")
        
    desativar_user.short_description = "Desativar usuários selecionados"