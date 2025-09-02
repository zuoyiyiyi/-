# 🎯 情感感知智能打卡机器人

一个基于 **情感分析** 和 **AI 智能提醒** 的目标打卡系统，融合用户身份管理、目标管理、打卡记录、情感聊天及个性化提醒功能。  
系统通过 **动态构建 Prompt 参数**，调用 **AI 大模型（Hugging Face API）** 生成高质量的打卡引导语，结合 **SnowNLP** 实时分析用户情绪，更精准地引导用户完成每日打卡。

---

## 🏗️ 项目结构

```


├── app.py                # 后端主程序入口
├── manage.py             # Django 管理命令入口
├── requirements.txt      # Python 依赖包列表
├── database.db / db.sqlite3  # SQLite 数据库文件
├── database.py           # 数据库访问逻辑封装
├── models.py             # ORM 模型定义
├── backend/              # 后端核心代码
│   ├── api/              # REST API 接口实现
│   └── ai_service.py     # AI 服务层（Prompt + AI接口）
├── frontend/ (Vue 项目)
│   ├── src/
│   │   ├── components/   # Vue 组件（聊天窗口、目标列表、打卡界面等）
│   │   ├── App.vue       # Vue 根组件
│   │   └── main.js       # Vue 入口文件
│   ├── public/           # 静态资源
│   ├── package.json      # 前端依赖配置
│   └── vue.config.js     # Vue CLI 配置
├── venv/                 # Python 虚拟环境
├── .env                  # 环境变量配置
├── docs/                 # 文档
│   ├── README.md
│   ├── DEBUG GUIDE.md
│   ├── QUICK START.md
│   ├── testcase-rule1.mdc
│   └── test-case-design.mdc
└── tests/                # 测试页面与用例
├── test_login.html
└── test_register.html

````

---

## ⚙️ 核心功能

### 🔹 后端（Django）
- 用户注册 / 登录 / 权限管理  
- 目标创建 / 修改 / 删除  
- 打卡记录与查询  
- 情感分析（SnowNLP）  
- 聊天与 AI 个性化提醒  

### 🔹 AI 服务层
- **fill_prompt_template(template, context)**  
  根据上下文动态填充 Prompt 模板  
- **call_free_ai_api(prompt, headers, data)**  
  调用 Hugging Face 免费 API，返回生成内容  
- **generate_local_response(...)**  
  AI 调用失败时使用本地模板降级  
- **generate_reminder_message(...)**  
  结合用户数据与历史打卡，生成个性化提醒  
- **generate_motivational_mes(...)**  
  基于 AI 内容生成激励语句，提升用户体验  

### 🔹 前端（Vue 2）
- 响应式页面布局  
- 打卡界面 / 目标管理 / 聊天窗口  
- 通过 **axios** 调用后端 REST API  
- 实时交互与情绪反馈  

### 🔹 测试与文档
- 提供详细的 **测试用例设计文档**  
- **调试指南** 和 **快速启动说明**  
- 前端测试页面（登录、注册）  

---

## 📦 技术栈

- **后端**：Django, SQLite, SnowNLP  
- **AI 服务**：Hugging Face API, Prompt Engineering  
- **前端**：Vue 2, Axios, Vue CLI  
- **测试**：HTML 测试页面, 用例文档  
- **环境管理**：Python venv, dotenv  

---

## 🚀 快速启动

### 后端
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 启动服务
python manage.py runserver
````

### 前端

```bash
cd frontend
npm install
npm run serve
```

访问：
👉 前端：[http://localhost:8080](http://localhost:8080)
👉 后端：[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📖 文档

* [调试指南 (DEBUG GUIDE)](./docs/DEBUG%20GUIDE.md)
* [快速启动 (QUICK START)](./docs/QUICK%20START.md)
* [测试用例设计 (test-case-design.mdc)](./docs/test-case-design.mdc)

---

## 🎯 总结

* **后端**：基于 Django，负责用户、目标、打卡、聊天和 AI 智能提醒接口
* **AI 层**：动态 Prompt 构建 + Hugging Face API 调用，支持本地模板降级
* **前端**：Vue 2 构建交互式页面，支持目标管理、打卡和情绪反馈
* **测试**：完善的测试文档和页面，保障功能稳定
