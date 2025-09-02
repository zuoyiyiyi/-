from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
import json
from snownlp import SnowNLP

from .models import User, Channel, Message, Goal, CheckIn, PromptTemplate, AIMessage
from .serializers import (
    UserSerializer, ChannelSerializer, MessageSerializer, 
    GoalSerializer, CheckInSerializer, PromptTemplateSerializer, AIMessageSerializer,
    GoalCreateSerializer, CheckInCreateSerializer, AIMessageCreateSerializer
)
from .ai_service import AIService

# Create your views here.

# 初始化AI服务
ai_service = AIService()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # type: ignore
    serializer_class = UserSerializer

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()  # type: ignore
    serializer_class = ChannelSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all() # type: ignore
    serializer_class = MessageSerializer

# 用户相关视图
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册"""
    data = request.data
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return Response({'error': '用户名和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create(
        username=username,
        password=make_password(password)
    )
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录"""
    data = request.data
    username = data.get('username')
    password = data.get('password')
    
    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

# 目标管理视图
@api_view(['GET', 'POST'])
def goals(request):
    """获取用户目标列表或创建新目标"""
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'error': '用户ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        goals = Goal.objects.filter(user_id=user_id, is_active=True)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        user_id = data.get('user_id')
        if not user_id:
            return Response({'error': '用户ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['user'] = user_id
        serializer = GoalCreateSerializer(data=data)
        if serializer.is_valid():
            goal = serializer.save(user_id=user_id)
            return Response(GoalSerializer(goal).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def goal_detail(request, goal_id):
    """获取、更新或删除特定目标"""
    goal = get_object_or_404(Goal, id=goal_id)
    
    if request.method == 'GET':
        serializer = GoalSerializer(goal)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = GoalCreateSerializer(goal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(GoalSerializer(goal).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        goal.is_active = False
        goal.save()
        return Response({'message': '目标已删除'})

# 打卡相关视图
@api_view(['GET', 'POST'])
def checkins(request):
    """获取打卡记录或创建新打卡"""
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        goal_id = request.GET.get('goal_id')
        
        if not user_id:
            return Response({'error': '用户ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        filters = {'user_id': user_id}
        if goal_id:
            filters['goal_id'] = goal_id
        
        checkins = CheckIn.objects.filter(**filters).order_by('-check_in_date')
        serializer = CheckInSerializer(checkins, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        user_id = data.get('user_id')
        goal_id = data.get('goal_id')
        
        if not user_id or not goal_id:
            return Response({'error': '用户ID和目标ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查是否已经打卡
        check_in_date = data.get('check_in_date', date.today())
        if CheckIn.objects.filter(user_id=user_id, goal_id=goal_id, check_in_date=check_in_date).exists():
            return Response({'error': '今天已经打卡了'}, status=status.HTTP_400_BAD_REQUEST)
        
        data['user'] = user_id
        data['goal'] = goal_id
        serializer = CheckInCreateSerializer(data=data)
        
        if serializer.is_valid():
            checkin = serializer.save(user_id=user_id, goal_id=goal_id)
            
            # 生成AI激励消息
            user = User.objects.get(id=user_id)
            goal = Goal.objects.get(id=goal_id)
            ai_message = ai_service.generate_motivational_message(user, goal, checkin)
            
            return Response({
                'checkin': CheckInSerializer(checkin).data,
                'ai_message': ai_message
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def checkin_stats(request):
    """获取打卡统计信息"""
    user_id = request.GET.get('user_id')
    goal_id = request.GET.get('goal_id')
    
    if not user_id:
        return Response({'error': '用户ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    filters = {'user_id': user_id}
    if goal_id:
        filters['goal_id'] = goal_id
    
    checkins = CheckIn.objects.filter(**filters)
    
    # 计算统计信息
    total_checkins = checkins.count()
    today = date.today()
    today_checkin = checkins.filter(check_in_date=today).exists()
    
    # 计算连续打卡天数
    consecutive_days = 0
    check_date = today
    while True:
        if checkins.filter(check_in_date=check_date).exists():
            consecutive_days += 1
            check_date -= timezone.timedelta(days=1)
        else:
            break
    
    # 最近7天打卡情况
    recent_checkins = []
    for i in range(7):
        check_date = today - timezone.timedelta(days=i)
        recent_checkins.append({
            'date': check_date.strftime('%Y-%m-%d'),
            'checked': checkins.filter(check_in_date=check_date).exists()
        })
    
    return Response({
        'total_checkins': total_checkins,
        'consecutive_days': consecutive_days,
        'today_checkin': today_checkin,
        'recent_checkins': recent_checkins
    })

# AI消息相关视图
@api_view(['POST'])
def generate_reminder(request):
    """生成AI提醒消息"""
    data = request.data
    user_id = data.get('user_id')
    goal_id = data.get('goal_id')
    
    if not user_id or not goal_id:
        return Response({'error': '用户ID和目标ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        goal = Goal.objects.get(id=goal_id)
        
        ai_message = ai_service.generate_reminder_message(user, goal)
        
        return Response({
            'ai_message': ai_message,
            'user': UserSerializer(user).data,
            'goal': GoalSerializer(goal).data
        })
        
    except (User.DoesNotExist, Goal.DoesNotExist):
        return Response({'error': '用户或目标不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def ai_messages(request):
    """获取AI消息历史"""
    user_id = request.GET.get('user_id')
    goal_id = request.GET.get('goal_id')
    
    if not user_id:
        return Response({'error': '用户ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    filters = {'user_id': user_id}
    if goal_id:
        filters['goal_id'] = goal_id
    
    ai_messages = AIMessage.objects.filter(**filters).order_by('-created_at')
    serializer = AIMessageSerializer(ai_messages, many=True)
    return Response(serializer.data)

# 消息相关视图（扩展原有功能）
@api_view(['POST'])
def send_message(request):
    """发送消息（扩展情感分析功能）"""
    data = request.data
    message_text = data.get('message')
    from_user_id = data.get('from_user')
    to_user_id = data.get('to_user')
    channel_id = data.get('channel')
    
    if not all([message_text, from_user_id, to_user_id, channel_id]):
        return Response({'error': '所有字段都是必需的'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 进行情感分析
    sentiment_result = ai_service.analyze_sentiment(message_text)
    
    message = Message.objects.create(
        message=message_text,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        channel_id=channel_id,
        sentiment_score=sentiment_result['score'],
        sentiment_label=sentiment_result['label']
    )
    
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_messages(request):
    """获取消息列表"""
    channel_id = request.GET.get('channel')
    if not channel_id:
        return Response({'error': '频道ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    messages = Message.objects.filter(channel_id=channel_id).order_by('created_at')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

# 提示词模板管理视图
@api_view(['GET', 'POST'])
def prompt_templates(request):
    """获取或创建提示词模板"""
    if request.method == 'GET':
        templates = PromptTemplate.objects.filter(is_active=True)
        serializer = PromptTemplateSerializer(templates, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PromptTemplateSerializer(data=request.data)
        if serializer.is_valid():
            template = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def prompt_template_detail(request, template_id):
    """获取、更新或删除提示词模板"""
    template = get_object_or_404(PromptTemplate, id=template_id)
    
    if request.method == 'GET':
        serializer = PromptTemplateSerializer(template)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PromptTemplateSerializer(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        template.is_active = False
        template.save()
        return Response({'message': '模板已删除'})

@api_view(['POST'])
@permission_classes([AllowAny])
def request_chat(request):
    """创建或获取两个用户之间的唯一聊天频道（顺序无关）"""
    from_user_id = int(request.data.get('from_user'))
    to_user_id = int(request.data.get('to_user'))
    if not from_user_id or not to_user_id:
        return Response({'error': 'from_user和to_user为必填'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 用排序保证顺序无关
    user_ids = sorted([from_user_id, to_user_id])
    channel = Channel.objects.filter(from_user_id=user_ids[0], to_user_id=user_ids[1]).first()
    if not channel:
        from_user = User.objects.get(id=user_ids[0])
        to_user = User.objects.get(id=user_ids[1])
        channel = Channel.objects.create(
            name=f"{from_user.username}-{to_user.username}",
            from_user=from_user,
            to_user=to_user
        )
    return Response({
        'channel_id': channel.id,
        'channel_name': channel.name
    })

@api_view(['GET'])
def batch_reminders(request):
    """批量获取所有目标的AI提示语，区分已打卡/未打卡"""
    user_id = request.GET.get('user_id')
    if not user_id:
        return Response({'error': '用户ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    today = date.today()
    goals = Goal.objects.filter(user_id=user_id, is_active=True)
    result = []
    for goal in goals:
        checked = CheckIn.objects.filter(user_id=user_id, goal_id=goal.id, check_in_date=today).exists()
        if checked:
            ai_reminder = f"太棒了，今天已经完成{goal.title}，继续保持！"
        else:
            ai_reminder = AIService().generate_reminder_message(goal.user, goal)
        result.append({
            'goal_id': goal.id,
            'title': goal.title,
            'checked': checked,
            'ai_reminder': ai_reminder
        })
    return Response(result)
