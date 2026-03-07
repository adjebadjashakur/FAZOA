from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin de base pour vérifier les rôles."""
    allowed_roles = []

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.role in self.allowed_roles

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        raise PermissionDenied


class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN']


class AdminOrSecretaryMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN', 'SECRETARY']


class AdminOrStockMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN', 'STOCK_MANAGER']


class AdminOrProductionMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN', 'PRODUCTION_MANAGER']


class AllStaffMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN', 'SECRETARY', 'STOCK_MANAGER', 'PRODUCTION_MANAGER']
