from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from accounts.managers import UserManager
from django.utils.text import slugify

# Create your models here.

# User Role Table.
class Role(models.Model):
    Admin = 1
    User = 2
    ROLE_CHOICES = [
        (Admin, 'Admin'),
        (User, 'User'),
    ]
    role = models.CharField(
        max_length=10,
        default='User',
        null=False
    )

    class Meta:
        db_table = "user_roles"

    def __str__(self):
        return self.role



### User Model
class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # this now over rides the username field and now email is the default field
    # REQUIRED_FIELDS = [] if you add another field and need it to be required, include it in the list

    objects = UserManager()

    class Meta:
        db_table = 'users'
        ordering = ('-timestamp', )
        indexes = [
            models.Index(fields=['name','email',]),
        ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    """@property
    def is_active(self):
        return self.is_active"""

## Question Set Model Here.

class QuestionSet(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    enable_negative_marking = models.BooleanField(default=False)
    negative_marking_percentage = models.IntegerField(blank=True, null=True)
    ideal_timeto_complete = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'questions_set'
        ordering = ('-created_on', )
        indexes = [
            models.Index(fields=['name','slug',]),
        ]
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

### Question Model Here.
class Question(models.Model):
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE,blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to ='question/', null=True, blank=True)
    QUEST_CHOICES = [
        ('Radio', 'Radio'),
        ('CheckBox', 'CheckBox'),
        ('Matrix', 'Matrix'),
    ]
    type = models.CharField(max_length=15,choices=QUEST_CHOICES,default='Radio',null=False)
    order = models.IntegerField(blank=True,null=True)
    marks = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        db_table = 'questions'
        ordering = ('-created_on', )
        indexes = [
            models.Index(fields=['question_set',]),
        ]

### Question Options Model Here.
class QuestionOptions(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to ='question/options/', null=True, blank=True)
    order = models.IntegerField(blank=True,null=True)
    marks = models.IntegerField(blank=True, null=True)
    answer = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question_options'
        ordering = ('-created_on', )
        indexes = [
            models.Index(fields=['question',]),
        ]

