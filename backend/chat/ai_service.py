import requests
import json
from typing import Dict, Any, Optional
from django.conf import settings
from .models import Goal, CheckIn, Message, User, PromptTemplate, AIMessage
from datetime import datetime, timedelta
from snownlp import SnowNLP

class AIService:
    """AI服务类，处理AI大模型调用和提示词模板"""
    
    def __init__(self):
        # 使用Hugging Face免费API
        self.api_key = getattr(settings, 'HUGGINGFACE_API_KEY', 'hf_xxx')  # 免费获取
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        self.fallback_api_url = "https://api-inference.huggingface.co/models/gpt2"
        
        # 备用方案：使用本地模板生成
        self.use_local_templates = True
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """分析文本情感"""
        try:
            s = SnowNLP(text)
            sentiment_score = s.sentiments  # 0-1之间，越接近1越正面
            
            # 将0-1的分数转换为-1到1的分数
            normalized_score = (sentiment_score - 0.5) * 2
            
            # 确定情感标签
            if sentiment_score > 0.7:
                sentiment_label = "positive"
            elif sentiment_score < 0.3:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            return {
                'score': normalized_score,
                'label': sentiment_label,
                'confidence': sentiment_score
            }
        except Exception as e:
            print(f"情感分析错误: {e}")
            return {
                'score': 0.0,
                'label': 'neutral',
                'confidence': 0.5
            }
    
    def get_user_context(self, user: User, goal: Goal) -> Dict[str, Any]:
        """获取用户上下文信息"""
        today = datetime.now().date()
        
        # 获取最近的打卡记录
        recent_checkins = CheckIn.objects.filter(
            user=user, 
            goal=goal
        ).order_by('-check_in_date')[:7]  # 最近7天
        
        # 计算连续打卡天数
        consecutive_days = 0
        check_date = today
        while True:
            if CheckIn.objects.filter(user=user, goal=goal, check_in_date=check_date).exists():
                consecutive_days += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        # 获取最近的消息情感分析
        recent_messages = Message.objects.filter(
            from_user=user
        ).order_by('-created_at')[:10]  # 最近10条消息
        
        avg_sentiment = 0
        if recent_messages:
            sentiment_scores = [msg.sentiment_score for msg in recent_messages if msg.sentiment_score is not None]
            if sentiment_scores:
                avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        
        # 计算最近未打卡天数
        last_checkin = recent_checkins.first()
        days_since_last = 0
        if last_checkin:
            days_since_last = (today - last_checkin.check_in_date).days
        
        return {
            'username': user.username,
            'goal_title': goal.title,
            'goal_description': goal.description,
            'consecutive_days': consecutive_days,
            'days_since_last_checkin': days_since_last,
            'recent_checkins_count': recent_checkins.count(),
            'avg_sentiment': avg_sentiment,
            'today': today.strftime('%Y-%m-%d'),
            'recent_checkins': [
                {
                    'date': checkin.check_in_date.strftime('%Y-%m-%d'),
                    'notes': checkin.notes,
                    'mood_score': checkin.mood_score
                }
                for checkin in recent_checkins
            ]
        }
    
    def fill_prompt_template(self, template: PromptTemplate, context: Dict[str, Any]) -> str:
        """填充提示词模板"""
        filled_prompt = template.template_content
        
        # 替换模板变量
        for variable in template.variables:
            if variable in context:
                placeholder = f"{{{variable}}}"
                filled_prompt = filled_prompt.replace(placeholder, str(context[variable]))
        
        return filled_prompt
    
    def call_free_ai_api(self, prompt: str) -> str:
        """调用免费AI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'inputs': prompt,
                'parameters': {
                    'max_length': 100,
                    'temperature': 0.7,
                    'do_sample': True
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').strip()
                return result.get('generated_text', '').strip()
            else:
                print(f"免费AI API调用失败: {response.status_code} - {response.text}")
                return self.generate_local_response(prompt)
                
        except Exception as e:
            print(f"免费AI API调用异常: {e}")
            return self.generate_local_response(prompt)
    
    def generate_local_response(self, prompt: str) -> str:
        """本地生成回复（备用方案）"""
        # 基于关键词和模板生成回复
        keywords = {
            '阅读': ['今天也要坚持阅读哦！', '翻开书本就是胜利！', '知识就是力量，继续加油！'],
            '运动': ['运动让生活更美好！', '坚持运动，健康生活！', '今天的汗水是明天的收获！'],
            '学习': ['学习使人进步！', '知识改变命运！', '今天的努力是明天的成功！'],
            '工作': ['工作顺利，心情愉快！', '专注工作，成就梦想！', '今天的付出是明天的收获！'],
            '打卡': ['打卡成功！继续保持！', '坚持就是胜利！', '每天进步一点点！'],
            '加油': ['加油！你是最棒的！', '相信自己，你能行！', '坚持就是胜利！']
        }
        
        # 根据提示词内容选择合适的回复
        for keyword, responses in keywords.items():
            if keyword in prompt:
                import random
                return random.choice(responses)
        
        # 默认回复
        default_responses = [
            "继续保持这个好习惯！",
            "坚持就是胜利！",
            "每天进步一点点！",
            "你是最棒的！",
            "加油！你能行！",
            "继续保持！",
            "太棒了！",
            "继续努力！"
        ]
        
        import random
        return random.choice(default_responses)
    
    def generate_reminder_message(self, user: User, goal: Goal) -> str:
        """生成提醒消息（用产品Prompt+业务数据+免费大模型）"""
        try:
            # 统计历史打卡
            today = datetime.now().date()
            recent_checkins = CheckIn.objects.filter(user=user, goal=goal).order_by('-check_in_date')[:3]
            if not recent_checkins:
                history_str = "最近3天均未打卡"
            else:
                days = [c.check_in_date.strftime('%Y-%m-%d') for c in recent_checkins]
                history_str = f"最近3天已打卡：{'、'.join(days)}"
            prompt = f'''
作为健身教练，请用温暖风格提醒用户：
{user.username}设置了目标{goal.title}，
最近打卡记录：{history_str}.
请生成30字内的鼓励语。
'''
            # 优先用Hugging Face免费API
            ai_response = self.call_free_ai_api(prompt)
            if not ai_response or len(ai_response) < 5:
                ai_response = self.generate_local_response(prompt)
            # 保存AI消息记录
            AIMessage.objects.create(
                user=user,
                goal=goal,
                prompt_template=None,
                filled_prompt=prompt,
                ai_response=ai_response,
                context_data={
                    'username': user.username,
                    'goal_title': goal.title,
                    'history_str': history_str
                }
            )
            return ai_response
        except Exception as e:
            print(f"生成提醒消息失败: {e}")
            return f"嗨 {user.username}，记得今天要{goal.title}哦！加油！"
    
    def generate_motivational_message(self, user: User, goal: Goal, checkin: CheckIn) -> str:
        """生成激励消息（打卡后）"""
        try:
            context = self.get_user_context(user, goal)
            context['mood_score'] = checkin.mood_score
            context['checkin_notes'] = checkin.notes
            
            template = PromptTemplate.objects.filter(
                name='motivational_message',
                is_active=True
            ).first()
            
            if not template:
                template = PromptTemplate.objects.create(
                    name='motivational_message',
                    description='打卡后激励消息模板',
                    template_content="""用户刚刚完成了目标"{goal_title}"的打卡！
用户名：{username}
连续打卡天数：{consecutive_days}天
心情评分：{mood_score}/10
打卡备注：{checkin_notes}

请生成一段30字内的激励话语，肯定用户的努力并鼓励继续坚持。""",
                    variables=['username', 'goal_title', 'consecutive_days', 'mood_score', 'checkin_notes']
                )
            
            filled_prompt = self.fill_prompt_template(template, context)
            
            if self.use_local_templates:
                ai_response = self.generate_local_response(filled_prompt)
            else:
                ai_response = self.call_free_ai_api(filled_prompt)
            
            AIMessage.objects.create(
                user=user,
                goal=goal,
                prompt_template=template,
                filled_prompt=filled_prompt,
                ai_response=ai_response,
                context_data=context
            )
            
            return ai_response
            
        except Exception as e:
            print(f"生成激励消息失败: {e}")
            return f"太棒了 {user.username}！你又完成了一次{goal.title}，继续保持！" 