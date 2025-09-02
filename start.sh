#!/bin/bash

echo "🚀 启动情感感知打卡机器人..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# 激活虚拟环境并启动后端
echo "📡 启动后端服务 (Django)..."
cd backend
source ../venv/bin/activate
python manage.py runserver --noreload &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端服务 (Vue.js)..."
export NODE_OPTIONS="--openssl-legacy-provider"
npm run serve &
FRONTEND_PID=$!

echo "✅ 服务启动完成！"
echo "📱 前端地址: http://localhost:8084 (或自动分配的端口)"
echo "🔧 后端地址: http://localhost:8000"
echo ""
echo "🧪 测试注册功能:"
echo "   1. 访问前端: http://localhost:8084"
echo "   2. 或使用测试页面: open simple_test.html"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait 