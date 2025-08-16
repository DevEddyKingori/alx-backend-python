from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from .filters import MessageFilter
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, MessageCreateSerializer
from .permissions import IsParticipantOfConversation
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Only participants can access their conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        """Return conversations where current user is a participant."""
        return self.queryset.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')

    def perform_create(self, serializer):
        """Create conversation and add current user as participant."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add participant to conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            if not conversation.participants.filter(id=self.request.user.id).exists():
                raise PermissionDenied("You must be a participant to add others")
            conversation.participants.add(user)
            return Response({'status': 'participant added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages in a conversation.
    Only participants can access and send messages.
    """
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    pagination_class = PageNumberPagination
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        """Return messages for conversations where user is a participant."""
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')

    def get_serializer_class(self):
        """Use different serializer for creation."""
        if self.action in ['create', 'update', 'partial_update']:
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        """Set sender and conversation for new messages."""
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(
            Conversation.objects.filter(participants=self.request.user),
            id=conversation_id
        )
        serializer.save(sender=self.request.user, conversation=conversation)

    def handle_exception(self, exc):
        """Handle permission denied exceptions with proper 403 responses"""
        if isinstance(exc, PermissionDenied):
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)
