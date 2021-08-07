# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt import tokens
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

""" 
build custom user modul manager :
to build or ovveried funs that comonly get used
in this case create new user and create superuser
"""

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an emil adress.')
        elif not username:
            raise ValueError('User must have a username.')
        user = self.model( # model is the model that we mannage trough this class
            email = self.normalize_email(email), # set it lowercase so we dont want it to be senstive
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email), # set it lowercase so we dont want it to be senstive
            username = username,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db) # means that we will the same db 
        return user
        
class User(AbstractBaseUser):

    """ 

    all those field are in AbstractBaseUser
    so to use them in the way we want we need
    to overide them 
    
    """

    def get_upolad_to_image_path(self):
        return f'profile_pics/{self.pk}/'

    email = models.EmailField(
        verbose_name='email',
        max_length=60,
        unique=True
        )
    username = models.CharField(
        max_length=30,
        unique=True
    )
    data_joined = models.DateTimeField(
        verbose_name='date joined',
        auto_now_add=True
        )
    last_login = models.DateTimeField(
        verbose_name='last login',
        auto_now=True
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    profile_image = models.ImageField(
        upload_to = get_upolad_to_image_path,
        null = True, blank = True,
        default='default_profile_pic.png'
    )

    objects = MyAccountManager() # link the user modul manager with the modul

    """refferance to the email field that we ovveride up, so instance 
    of useing username to login we will user email"""

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    """ now lets add permession or edit them from the
    base user model by overiding """

    # check if user is admin before doing any thing that reuired admin perm
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
     
    def tokens(self):
        return {
            'refresh': str(tokens.RefreshToken.for_user(self)),
            'access' : str(tokens.RefreshToken.for_user(self).access_token)
        }

# class UserManager(BaseUserManager):
#     def create_user(self, email, username,  password=None):
#         if not email:
#             raise KeyError('user must have an email')
#         if not username:
#             raise KeyError('user must have a username')
        

#         user = self.model(email=self.normalize_email(email), username=username)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username,  password):
       
#         user = self.create_user(email, username,  password)
#         user.is_admin = True
#         user.is_staff = True
#         user.superuser = True
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=50, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_verified = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REAUIRED_FIELDS = ['username',]
    
#     def __str__(self):
#         return self.username

    # def tokens(self):
    #     return {
    #         'refresh': str(tokens.RefreshToken.for_user(self)),
    #         'access' : str(tokens.RefreshToken.for_user(self).access_token)
    #     }
