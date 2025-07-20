import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timezone


# Custom User model extending Django's AbstractUser.
class User(AbstractUser):
    """
    Includes all required fields while maintaining built-in auth functionality.
    """
    # Primary key (user_id equivalent)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="User ID"
    )

    # Required fields (AbstractUser already includes username and password)
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

    # Optional fields
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    online_status = models.BooleanField(
        default=False,
        help_text="Designates whether the user is currently online."
    )
    last_seen = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time the user was active."
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="Brief description about yourself."
    )

    # Authentication configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def save(self, *args, **kwargs):
        """Normalize email and handle username generation"""
        self.email = self.email.lower().strip()
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Return the first_name plus the last_name with a space in between."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user (first_name only)."""
        return self.first_name


# Model representing a conversation between users.
class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Conversation ID"
    )
    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_group_chat = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.is_group_chat and self.name:
            return f"Group: {self.name}"
        return f"Conversation ({self.conversation_id})"


# Model representing a message in a conversation.
class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Message ID"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_body = models.TextField(
        help_text="The content of the message"
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the message was sent"
    )
    read_by = models.ManyToManyField(
        User,
        related_name='read_messages',
        blank=True
    )

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"

    def mark_as_read(self, user):
        """
        Mark the message as read by a specific user.
        """
        if user not in self.read_by.all():
            self.read_by.add(user)
            self.conversation.updated_at = timezone.now()
            self.conversation.save()
