from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

# Create your models here.

class MyaccountManager(BaseUserManager):
    def create_user(self, first_name , last_name, username, email, password = None):

        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, first_name , last_name, username, email, password):

        user = self.create_user(
            email       = self.normalize_email(email),
            username    = username,
            password    = password,
            first_name  = first_name,
            last_name   = last_name,
        )

        user.is_admin        = True
        user.is_active       = True
        user.is_staff        = True
        user.is_superadmin   = True
        user.save(using = self._db)
        return user
        

class Account(AbstractBaseUser):

    first_name        = models.CharField(max_length = 50)
    last_name         = models.CharField(max_length = 50)
    username          = models.CharField(max_length = 50 , unique = True)
    email             = models.EmailField(max_length = 100 , unique = True)
    phone_number      = models.CharField(max_length = 50 , unique = True)


    # control:

    joined_at         = models.DateTimeField(auto_now_add = True) 
    last_login_at     = models.DateTimeField(auto_now_add = True)
    is_admin          = models.BooleanField(default = False)
    is_staff          = models.BooleanField(default = False)
    is_active         = models.BooleanField(default = False) 
    is_superadmin     = models.BooleanField(default = False)


    USERNAME_FIELD    = 'email'
    REQUIRED_FIELDS   = ['username', 'first_name', 'last_name']

    objects = MyaccountManager()

    def full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name
    

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True



# def uploaded_photos(instance , filename):
#     imagename , extension = filename.split('.')
#     return 'photos/Profile_Picture/%s.%s'%(instance.id ,extension)

class UserProfile(models.Model):
    user = models.OneToOneField(Account , on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length = 100 , blank= True)
    address_line2 = models.CharField(max_length = 100, blank = True)
    profile_image = models.ImageField(blank = True , upload_to='photos/Profile_Picture/')
    city = models.CharField(max_length = 20, blank = True)
    state = models.CharField(max_length = 20, blank = True)
    country = models.CharField(max_length = 20, blank = True)

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line1}, {self.address_line2}'


