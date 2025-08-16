from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'birth_date', 'online_status', 'last_seen']
        extra_kwargs = {
            'profile_picture': {'required': False},
            'bio': {'required': False},
            'birth_date': {'required': False},
        }

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    sender = UserSerializer(read_only=True)
    read_by = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp', 'read_by']
        read_only_fields = ['id', 'timestamp', 'sender', 'read_by']

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    """
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=True
    )
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    group_name = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'is_group_chat', 'group_name', 'messages', 'last_message']
        read_only_fields = ['id', 'created_at', 'updated_at', 'messages']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def validate(self, data):
        """
        Validate conversation data:
        - Group name is required for group chats
        - At least one other participant is required
        """
        if data.get('is_group_chat', False) and not data.get('group_name'):
            raise serializers.ValidationError({
                'group_name': 'Group name is required for group chats'
            })

        participants = data.get('participants', [])
        if len(participants) < 1:
            raise serializers.ValidationError({
                'participants': 'At least one participant is required'
            })

        return data

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.add(self.context['request'].user)
        for participant in participants:
            conversation.participants.add(participant)
        return conversation

class MessageCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        max_length=2000,
        trim_whitespace=True,
        required=True
    )

    class Meta:
        model = Message
        fields = ['content']

    def validate_content(self, value):
        """
        Validate message content is not empty
        """
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty")
        return value.strip()