from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'librarian'),
)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'Admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Поля не обязательны при создании через createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        created_ts = int(self.created_at.timestamp()) if self.created_at else ''
        updated_ts = int(self.updated_at.timestamp()) if self.updated_at else ''
        return f"'id': {self.id}, 'first_name': '{self.first_name}', 'middle_name': '{self.middle_name}', 'last_name': '{self.last_name}', 'email': '{self.email}', 'created_at': {created_ts}, 'updated_at': {updated_ts}, 'role': {self.role}, 'is_active': {self.is_active}"

    def __repr__(self):
        return f"{CustomUser.__name__}(id={self.id})"

    @classmethod
    def get_by_id(cls, user_id):
        return cls.objects.filter(id=user_id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.objects.filter(email=email).first()

    @classmethod
    def delete_by_id(cls, user_id):
        user_to_delete = cls.objects.filter(id=user_id).first()
        if user_to_delete:
            user_to_delete.delete()
            return True
        return False

    @classmethod
    def create(cls, email, password, first_name=None, middle_name=None, last_name=None):
        if CustomUser.objects.filter(email=email).exists():
            return None

        user = cls.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name
        )
        return user

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'role': self.role,
            'is_active': self.is_active
        }

    def update(self, first_name=None, last_name=None, middle_name=None, password=None, role=None, is_active=None):
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if middle_name is not None:
            self.middle_name = middle_name
        if password is not None:
            self.set_password(password)
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        self.save()

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    def get_role_name(self):
        return self.get_role_display()