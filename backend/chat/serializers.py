from rest_framework import serializers
from .models import User, Channel, Message, Goal, CheckIn, PromptTemplate, AIMessage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'created_at', 'reminder_time', 'timezone']
        read_only_fields = ['id', 'created_at']

class ChannelSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Channel
        fields = ['id', 'name', 'from_user', 'to_user']

class MessageSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'message', 'from_user', 'to_user', 'channel', 'created_at', 'sentiment_score', 'sentiment_label']

class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'frequency', 'target_count', 'is_active', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CheckInSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)
    
    class Meta:
        model = CheckIn
        fields = ['id', 'user', 'goal', 'check_in_date', 'check_in_time', 'notes', 'mood_score']
        read_only_fields = ['id', 'check_in_time']

class PromptTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptTemplate
        fields = ['id', 'name', 'description', 'template_content', 'variables', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class AIMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)
    prompt_template = PromptTemplateSerializer(read_only=True)
    
    class Meta:
        model = AIMessage
        fields = ['id', 'user', 'goal', 'prompt_template', 'filled_prompt', 'ai_response', 'context_data', 'created_at']
        read_only_fields = ['id', 'created_at']

# 用于创建和更新的序列化器
class GoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'frequency', 'target_count', 'is_active']

class CheckInCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = ['goal', 'check_in_date', 'notes', 'mood_score']

class AIMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMessage
        fields = ['goal', 'prompt_template', 'filled_prompt', 'ai_response', 'context_data'] 