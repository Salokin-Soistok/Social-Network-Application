from django.db import models  # Import the models module from Django
from django.utils import timezone  # Import timezone for date/time handling
from django.contrib.auth.models import User  # Import the User model for authentication
from django.db.models.signals import post_save  # Import signal to hook into model save events
from django.dispatch import receiver  # Import receiver to handle signals

class Post(models.Model):  # Define the Post model
    body = models.TextField()  # The content of the post
    created_on = models.DateTimeField(default=timezone.now)  # Timestamp when the post is created
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the User who created the post
    likes = models.ManyToManyField(User, blank=True, related_name='likes')  # Users who liked the post
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')  # Users who disliked the post

class Comment(models.Model):  # Define the Comment model
    comment = models.TextField()  # The content of the comment
    created_on = models.DateTimeField(default=timezone.now)  # Timestamp when the comment is created
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the User who wrote the comment
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # Reference to the Post this comment belongs to

class UserProfile(models.Model):  # Define the UserProfile model
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)  # One-to-one relationship with User
    name = models.CharField(max_length=30, blank=True, null=True)  # Optional name field
    bio = models.TextField(max_length=500, blank=True, null=True)  # Optional bio field
    birth_date = models.DateField(null=True, blank=True)  # Optional birth date
    location = models.CharField(max_length=100, blank=True, null=True)  # Optional location
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True, null=True)  # Profile picture with a default image
    followers = models.ManyToManyField(User, blank=True, related_name='followers')  # Users who follow this profile

@receiver(post_save, sender=User)  # Signal to create a UserProfile when a User is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # Create a UserProfile for the new User

@receiver(post_save, sender=User)  # Signal to save the UserProfile when a User is saved
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # Save the UserProfile associated with the User
