from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrateur"
        SECRETARY = "SECRETARY", "Secrétaire"
        STOCK_MANAGER = "STOCK_MANAGER", "Responsable Stock"
        PRODUCTION_MANAGER = "PRODUCTION_MANAGER", "Responsable Production"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SECRETARY,
        verbose_name='Rôle'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Téléphone')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_secretary(self):
        return self.role == self.Role.SECRETARY

    @property
    def is_stock_manager(self):
        return self.role == self.Role.STOCK_MANAGER

    @property
    def is_production_manager(self):
        return self.role == self.Role.PRODUCTION_MANAGER
