# OpenAI API密钥配置指南

## 🔑 获取OpenAI API密钥

### 1. 注册OpenAI账户
- 访问 [OpenAI官网](https://platform.openai.com/)
- 点击右上角"Sign up"注册账户
- 可以使用邮箱或Google账户注册

### 2. 获取API密钥
1. 登录后，点击左侧菜单的"API Keys"
2. 点击"Create new secret key"
3. 给密钥起个名字（比如"打卡机器人"）
4. **重要**: 复制生成的密钥（密钥只显示一次！）

### 3. 查看API使用情况
- 在"Usage"页面可以查看API使用量和费用
- OpenAI提供免费额度（通常是$5或$18）
- 超出免费额度后按使用量收费

## ⚙️ 配置到项目中

### 方法1：使用环境变量（推荐）

1. 在backend目录下创建`.env`文件：
```bash
cd backend
touch .env
```

2. 在`.env`文件中添加您的API密钥：
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. 启动服务器时会自动读取环境变量

### 方法2：直接修改settings.py

1. 打开`backend/backend/settings.py`
2. 找到AI配置部分
3. 将`AI_API_KEY`的值替换为您的实际密钥：
```python
AI_API_KEY = 'sk-your-actual-api-key-here'
```

## 🧪 测试配置

配置完成后，启动服务器：
```bash
python manage.py runserver
```

如果看到以下信息，说明配置成功：
```
Django version 5.2.3, using settings 'backend.settings'
Starting development server at http://127.0.0.1:8000/
```

如果看到警告信息，说明需要配置API密钥。

## 🔒 安全注意事项

1. **不要提交API密钥到Git**：
   - 确保`.env`文件在`.gitignore`中
   - 不要在代码中硬编码密钥

2. **定期轮换密钥**：
   - 定期在OpenAI平台生成新密钥
   - 删除不再使用的旧密钥

3. **监控使用量**：
   - 定期检查API使用情况
   - 设置使用量限制避免意外费用

## 💰 费用说明

- **免费额度**: OpenAI通常提供$5-$18的免费额度
- **收费标准**: 按token使用量收费
- **预估费用**: 本项目每次AI调用约$0.001-$0.01
- **监控**: 在OpenAI平台的"Usage"页面查看详细费用

## 🆘 常见问题

### Q: 密钥格式是什么样的？
A: OpenAI API密钥格式为：`sk-`开头，后面跟着一串字符

### Q: 如何检查密钥是否有效？
A: 可以访问 https://platform.openai.com/api-keys 查看密钥状态

### Q: 密钥泄露了怎么办？
A: 立即在OpenAI平台删除该密钥并生成新的

### Q: 免费额度用完了怎么办？
A: 需要在OpenAI平台添加支付方式，或使用其他AI服务提供商

## 📞 获取帮助

如果遇到问题：
1. 查看OpenAI官方文档：https://platform.openai.com/docs
2. 检查API密钥格式是否正确
3. 确认账户有足够的余额
4. 查看Django服务器日志获取详细错误信息 