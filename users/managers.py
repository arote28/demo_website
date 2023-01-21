from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import ASCIIUsernameValidator

class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app
    """
    #
    # def _create_user(self,email,password, **extra_fields):
    #     user = self.model(email=email, **extra_fields)
    #     # extra_fieldsif extra_fields['role'] == 1:
    #     #     extra_fields.setdefault('is_active',True)
    #     #     extra_fields.setdefault('is_superuser', True)
    #     #     user.set_password(password)
    #     #     user.save()
    #     #     return user
    #     # else:
    #     user.set_password(password)
    #     user.save()
    #     return user

    def create_user(self,email,password, **extra_fields):

        if not email:
            raise ValueError(_("The email must be set."))
        # if not extra_fields['username']:
        #     raise ValueError(_("The username must be set."))
        if not password:
            raise ValueError(_("The password must be set."))
        email = self.normalize_email(email)
        # import pdb;
        # pdb.set_trace()
        # if extra_fields['role'] == 1:
        #     extra_fields.setdefault('is_active', True)
        #     # extra_fields.setdefault('is_superuser', True)
        #     # extra_fields.setdefault('is_staff', True)
        #     extra_fields.setdefault('role', 1)
        #
        #     if extra_fields.get('role') != 1:
        #         raise ValueError('Superuser must have role of Global Admin')
        #     return self._create_user(email, password, **extra_fields)
        # else:
        if extra_fields['role'] == 1 or extra_fields['role'] == 2:
            # extra_fields.setdefault('role', extra_fields['role'])
            extra_fields.setdefault('is_staff', True)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        else:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self,email,password,**extra_fields):
        # user = self.create_user(email,password=password,**extra_fields)
        # user.is_admin = True
        # user.save(using=self._db)
        # return user

        # extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', 0)

        if extra_fields.get('role') != 0:
            raise ValueError('Superuser must have role of Global Admin')
        return self.create_user(email,password, **extra_fields)