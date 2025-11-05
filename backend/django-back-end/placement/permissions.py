# placement/permissions.py
from rest_framework import permissions
from core.permissions import IsProfessor, IsPDT, IsEscola, IsAdmin

class IsProfessorOrPDTOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            IsProfessor().has_permission(request, view) or
            IsPDT().has_permission(request, view) or
            IsAdmin().has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        return obj.escola.usuario == request.user or request.user.is_staff