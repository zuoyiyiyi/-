# 情感感知智能打卡机器人
该项目是一个基于情感分析和 AI 智能提醒的目标打卡系统，涵盖用户身份管理、目标管理、打卡记录、情感聊天及 AI 个性化提醒模块。团队通过动态构建 Prompt 参数，调用 AI 大模型生成高质量打卡引导语，结合 SnowNLP 实时分析用户情绪，更精准地引导用户完成每日打卡。
后端部分
•	核心入口和配置文件
o	app.py：后端主程序入口（可能是 Flask 或 Django 的启动脚本）
o	manage.py：典型 Django 管理命令入口，说明项目主要用 Django 作为后端框架
o	.env、env example.txt：环境变量配置文件，存放密钥、数据库连接等配置信息
o	requirements.txt：Python依赖包列表
•	数据库相关
o	database.db、db.sqlite3：SQLite数据库文件，存储用户数据、打卡记录等
o	database.py：数据库连接或操作逻辑（封装数据库访问接口）
o	models.py：Django ORM模型定义，定义用户、目标、打卡、聊天等实体数据结构
•	后端代码目录
o	backend/ 目录，里面包含后端主要代码，可能细分为各个功能子模块（如聊天、目标管理、AI服务等）
o	api/ 文件夹，存放接口实现代码（REST API视图、路由等）
•	AI相关服务
o	ai_service.py（或类似文件，含 fill_prompt_template、call_free_ai_api 等函数）
	负责动态构建 AI Prompt 模板
	调用 Hugging Face 免费AI接口
	实现本地模板降级（fallback）逻辑
	生成个性化提醒和激励语句
 
2. 前端部分
•	src/ 目录：Vue前端源码
o	components/：Vue组件，负责页面功能模块，如聊天窗口、目标列表、打卡界面等
o	App.vue：根组件，整个应用的顶层组件
o	main.js：入口文件，初始化Vue实例，配置路由和全局插件等
•	public/：静态资源目录（HTML模板、图片等）
•	node_modules/：依赖库
•	package.json 和 package-lock.json：前端依赖和项目配置
•	vue.config.js：Vue CLI配置文件，配置代理、打包选项等
 
3. 虚拟环境和配置
•	venv/：Python虚拟环境，隔离依赖
•	.env：环境变量配置，包含密钥、API地址等信息
 
4. 文档及测试
•	README.md、DEBUG GUIDE.md、QUICK START.md：项目说明、调试指南、快速启动说明
•	testcase-rule1.mdc、test-case-design.mdc：测试用例设计文档，说明项目测试流程和用例规则
•	test_login.html、test_register.html 等：前端或接口测试页面，用于调试登录、注册功能
 
5. 重要功能相关函数（ai_service.py等）
•	fill_prompt_template(template, context)：根据业务上下文，动态填充AI提示模板中的变量字段，生成完整的Prompt字符串
•	call_free_ai_api(prompt, headers, data)：调用免费AI接口（如Hugging Face），发送Prompt并返回AI生成结果
•	generate_local_response(prompt, keywords, responses)：当AI接口调用失败时，使用本地模板和关键词生成备用回答
•	generate_reminder_message(user, goal, today, recent_checkins, history_str, days, prompt)：结合用户数据和历史打卡，生成个性化的打卡提醒消息
•	generate_motivational_mes(user, goal, checkin, context, template, filled_prompt, ai_response)：基于AI返回内容生成激励语句，提升用户体验
 
总体总结
•	后端：基于 Django 框架，结合数据库 ORM，负责用户管理、目标管理、打卡记录、聊天消息、情感分析及AI智能提醒功能的接口开发。
•	AI 服务层：封装了动态 Prompt 构建和调用大模型API的逻辑，支持本地模板降级。
•	前端：Vue 2 实现响应式页面，包含聊天、目标管理、打卡管理等核心交互模块，通过 axios 与后端REST API通信。
•	测试和文档：项目配备测试设计文档和调试页面，保证开发质量和接口准确性。
<img width="432" height="640" alt="image" src="https://github.com/user-attachments/assets/a721c484-4b68-4d76-b74c-ca9a7dc8e4c1" />
