from django.db import models
from django.utils import timezone
import json

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 用户偏好设置
    reminder_time = models.TimeField(default='09:00:00')  # 每日提醒时间
    timezone = models.CharField(max_length=50, default='Asia/Shanghai')
    
    def __str__(self):
        return self.username

class Channel(models.Model):
    name = models.CharField(max_length=60)
    from_user = models.ForeignKey(User, related_name='channels_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='channels_to', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Message(models.Model):
    message = models.TextField()
    from_user = models.ForeignKey(User, related_name='messages_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='messages_to', on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 情感分析结果
    sentiment_score = models.FloatField(null=True, blank=True)  # 情感分数 (-1到1)
    sentiment_label = models.CharField(max_length=20, null=True, blank=True)  # 情感标签
    
    def __str__(self):
        return str(self.message)[:20]

class Goal(models.Model):
    """用户打卡目标"""
    user = models.ForeignKey(User, related_name='goals', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # 目标标题，如"每天阅读"
    description = models.TextField(blank=True)  # 目标描述
    frequency = models.CharField(max_length=20, default='daily')  # 频率：daily, weekly, monthly
    target_count = models.IntegerField(default=1)  # 目标次数
    is_active = models.BooleanField(default=True)  # 是否激活
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class CheckIn(models.Model):
    """打卡记录"""
    user = models.ForeignKey(User, related_name='checkins', on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, related_name='checkins', on_delete=models.CASCADE)
    check_in_date = models.DateField()  # 打卡日期
    check_in_time = models.DateTimeField(auto_now_add=True)  # 打卡时间
    notes = models.TextField(blank=True)  # 打卡备注
    mood_score = models.IntegerField(null=True, blank=True)  # 心情评分 1-10
    
    class Meta:
        unique_together = ['user', 'goal', 'check_in_date']  # 同一天同一目标只能打卡一次
    
    def __str__(self):
        return f"{self.user.username} - {self.goal.title} - {self.check_in_date}"

class PromptTemplate(models.Model):
    """AI提示词模板"""
    name = models.CharField(max_length=100)  # 模板名称
    description = models.TextField()  # 模板描述
    template_content = models.TextField()  # 模板内容
    variables = models.JSONField(default=list)  # 模板变量列表
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class AIMessage(models.Model):
    """AI生成的消息记录"""
    user = models.ForeignKey(User, related_name='ai_messages', on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, related_name='ai_messages', on_delete=models.CASCADE)
    prompt_template = models.ForeignKey(PromptTemplate, on_delete=models.CASCADE)
    filled_prompt = models.TextField()  # 填充后的提示词
    ai_response = models.TextField()  # AI回复内容
    context_data = models.JSONField(default=dict)  # 上下文数据
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"AI Message for {self.user.username} - {self.created_at}"
