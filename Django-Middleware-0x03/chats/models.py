import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes all required fields while maintaining built-in auth functionality.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="User ID"
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        null=False,
        help_text="Required. Must be a valid email address."
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False,
        null=False
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    online_status = models.BooleanField(
        default=False,
        help_text="User's online status."
    )
    last_seen = models.DateTimeField(
        default=datetime.now,
        help_text="Last time user was seen online."
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="Short bio for the user."
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        help_text="User's birth date."
    )

class Conversation(models.Model):
    """
    Model representing a chat conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    group_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)