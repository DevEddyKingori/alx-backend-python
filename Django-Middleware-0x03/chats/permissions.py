from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_permission(self, request, view):
        # Allow only authenticated users
        if not request.user.is_authenticated:
            return False

        # For conversation list/create, just check authentication
        if view.action in ['list', 'create']:
            return True

        # For other actions, check conversation participation
        conversation_id = view.kwargs.get('pk') or view.kwargs.get('conversation_id')
        if conversation_id:
            return Conversation.objects.filter(
                id=conversation_id,
                participants=request.user
            ).exists()
        return False

    def has_object_permission(self, request, view, obj):
        # For messages, check if user is participant in the conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(id=request.user.id).exists()
        # For conversations, check if user is participant
        return obj.participants.filter(id=request.user.id).exists()