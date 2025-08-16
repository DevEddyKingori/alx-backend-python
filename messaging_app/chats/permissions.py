from rest_framework import permissions
from .models import Conversation
from rest_framework.exceptions import PermissionDenied

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to:
    - Send (POST), view (GET), update (PUT/PATCH), and delete (DELETE) messages
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
            if not Conversation.objects.filter(
                id=conversation_id,
                participants=request.user
            ).exists():
                raise PermissionDenied("You are not a participant in this conversation")
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Explicitly check for PUT, PATCH, DELETE methods
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'conversation'):
                if not obj.conversation.participants.filter(id=request.user.id).exists():
                    raise PermissionDenied("You are not a participant in this conversation")
            elif not obj.participants.filter(id=request.user.id).exists():
                raise PermissionDenied("You are not a participant in this conversation")
        return True
