from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from .models import Message, Notification
from django.views.decorators.cache import cache_page

@login_required
def inbox_unread(request):
    """Display unread messages using custom managers with optimized queries"""
    unread_messages = Message.unread.unread_for_user(request.user)
    unread_notifications = Notification.objects.filter(
        user=request.user,
        read=False
    ).select_related('message__sender').only(
        'id', 'created_at', 'read', 
        'message__id', 'message__content', 'message__sender__username'
    )
    
    return render(request, 'messaging/inbox_unread.html', {
        'unread_messages': unread_messages,
        'unread_notifications': unread_notifications,
        'unread_count': unread_messages.count(),
        'notification_count': unread_notifications.count()
    })

@login_required
@cache_page(60)
def conversation_view(request, message_id):
    """View conversation thread with optimized queries"""
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').only(
            'id', 'content', 'timestamp', 
            'sender__username', 'receiver__username',
            'read', 'parent_message_id'
        ),
        Q(id=message_id),
        Q(sender=request.user) | Q(receiver=request.user)
    )
    message.mark_as_read()
    
    thread_messages = Message.objects.filter(
        Q(id=message.id) | 
        Q(parent_message=message.id) |
        Q(parent_message__parent_message=message.id)
    ).select_related(
        'sender', 'receiver', 'parent_message'
    ).only(
        'id', 'content', 'timestamp',
        'sender__username', 'receiver__username',
        'parent_message_id', 'read'
    ).order_by('timestamp')
    
    messages_dict = {m.id: {'message': m, 'replies': []} for m in thread_messages}
    thread_structure = []
    
    for m in thread_messages:
        if m.parent_message:
            messages_dict[m.parent_message.id]['replies'].append(messages_dict[m.id])
        else:
            thread_structure.append(messages_dict[m.id])

    return render(request, 'messaging/conversation.html', {
        'root_message': message,
        'thread_structure': thread_structure,
        'current_user': request.user
    })

@login_required
def notifications_view(request):
    """Display all notifications with optimized queries"""
    notifications = Notification.objects.filter(
        user=request.user
    ).select_related(
        'message', 'message__sender'
    ).only(
        'id', 'created_at', 'read',
        'message__id', 'message__content', 'message__sender__username'
    ).order_by('-created_at')
    
    return render(request, 'messaging/notifications.html', {
        'notifications': notifications
    })

@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(
        Notification.objects.only('id', 'read', 'message_id'),
        id=notification_id,
        user=request.user
    )
    notification.mark_as_read()
    return redirect(request.META.get('HTTP_REFERER', 'notifications'))

@login_required
def delete_user(request):
    """Handle user account deletion"""
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('home')
    return render(request, 'messaging/confirm_delete.html')
