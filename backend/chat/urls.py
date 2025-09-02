from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'channels', views.ChannelViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # 用户认证
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    # 目标管理
    path('goals/', views.goals, name='goals'),
    path('goals/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    
    # 打卡管理
    path('checkins/', views.checkins, name='checkins'),
    path('checkin-stats/', views.checkin_stats, name='checkin_stats'),
    
    # AI消息
    path('generate-reminder/', views.generate_reminder, name='generate_reminder'),
    path('ai-messages/', views.ai_messages, name='ai_messages'),
    
    # 消息管理（扩展原有功能）
    path('send-message/', views.send_message, name='send_message'),
    path('get-messages/', views.get_messages, name='get_messages'),
    
    # 提示词模板管理
    path('prompt-templates/', views.prompt_templates, name='prompt_templates'),
    path('prompt-templates/<int:template_id>/', views.prompt_template_detail, name='prompt_template_detail'),
    
    path('request_chat', views.request_chat, name='request_chat'),
    path('batch-reminders/', views.batch_reminders, name='batch_reminders'),
] 