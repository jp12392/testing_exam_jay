from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=True): # may look repetitive adding staff, admin and active status, but it simplifies the
                                                                                        # work when using create_staffuser() and create_superuser()
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError('User must have a password')
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        return self.create_user(email, password=password, is_staff=True)

    def create_superuser(self, email, password=None):
        return self.create_user(email, password=password, is_staff=True, is_admin=True)