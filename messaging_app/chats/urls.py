from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Create main router and register conversations
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create nested router for messages
messages_router = routers.NestedDefaultRouter(
    router, r'conversations', lookup='conversation')
messages_router.register(r'messages', MessageViewSet,
                         basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(messages_router.urls)),
]
