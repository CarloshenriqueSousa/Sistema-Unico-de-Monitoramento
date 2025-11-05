from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.db.models import JSONField


class UserQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(is_active=True)

    def por_tipo(self, tipo):
        return self.ativos().filter(user_type=tipo)


class ManageUser(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, identifier, password, **extra_fields):
        if not identifier:
            raise ValueError(_('O identificador deve ser definido'))

        user = self.model(identifier=identifier, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, identifier, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(identifier, password, **extra_fields)

    def create_superuser(self, identifier, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(identifier, password, email=email, **extra_fields)


# Atribui o QuerySet ao Manager
ManageUser = ManageUser.from_queryset(UserQuerySet)


class User(AbstractUser):
    USER_TYPES = [
        ("admin", "Admin"),
        ("escola", "Escola"),
        ("professor", "Professor"),
        ("aluno", "Aluno"),
        ("responsavel", "Responsável"),
    ]

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )

    identifier = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9#@_-]+$",
                message=_(
                    "O identificador deve conter apenas caracteres alfanuméricos, #, @, _ ou -."
                ),
                code="invalid_identifier",
            )
        ],
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )

    nome = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("nome de exibição"),
    )

    user_type = models.CharField(
        max_length=60,
        choices=USER_TYPES,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("ativo"),
    )

    is_staff = models.BooleanField(
        default=False,
    )

    metadata = JSONField(
        blank=True,
        null=True,
        verbose_name=_("metadados"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("criado em"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("atualizado em"),
    )

    history = HistoricalRecords(verbose_name=_("histórico"))

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_("The groups this user belongs to."),
        related_name="core_user_set",
        related_query_name="core_user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="core_user_set",
        related_query_name="core_user",
    )

    # Remove username herdado do AbstractUser
    username = None
    USERNAME_FIELD = "identifier"
    REQUIRED_FIELDS = ["email", "user_type"]

    objects = ManageUser()

    def __str__(self):
        return f"{self.get_user_type_display()} | {self.identifier}"

    def get_user_type_display(self):
        return dict(self.USER_TYPES).get(self.user_type, "Desconhecido")

    def get_prefix(self):
        return self.identifier[0] if self.identifier else None
