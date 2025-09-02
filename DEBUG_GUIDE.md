# 🔧 注册功能调试指南

## 问题描述
点击注册按钮没有反应

## 🔍 排查步骤

### 1. 检查浏览器控制台
1. 打开浏览器访问 http://localhost:8080
2. 按 F12 打开开发者工具
3. 点击 "Console" 标签
4. 尝试注册，查看是否有错误信息

### 2. 测试后端API
使用测试页面验证后端是否正常：
```bash
# 在浏览器中打开测试页面
open test_register.html
```

### 3. 检查网络请求
1. 在开发者工具中点击 "Network" 标签
2. 尝试注册
3. 查看是否有对 `/api/register/` 的请求
4. 检查请求状态码和响应内容

## 🛠️ 常见问题及解决方案

### 问题1：标签页切换不工作
**原因**: Bootstrap标签页依赖jQuery
**解决**: 已修复为Vue原生实现

### 问题2：axios请求失败
**原因**: axios配置问题
**解决**: 已修复Plugin定义

### 问题3：CORS跨域问题
**原因**: 前后端端口不同
**解决**: 后端已配置CORS

### 问题4：表单验证失败
**检查项**:
- 用户名不能为空
- 密码不能为空
- 确认密码必须与密码一致

## 🧪 手动测试

### 使用curl测试后端
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

### 使用fetch测试前端
在浏览器控制台中运行：
```javascript
fetch('http://localhost:8000/api/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'testuser2',
    password: 'testpass2'
  })
})
.then(response => response.json())
.then(data => console.log('Success:', data))
.catch(error => console.error('Error:', error));
```

## 📋 检查清单

- [ ] 前端服务运行在 http://localhost:8080
- [ ] 后端服务运行在 http://localhost:8000
- [ ] 浏览器控制台无错误
- [ ] 网络请求正常发送
- [ ] 后端API返回正确响应
- [ ] 表单验证通过

## 🆘 如果问题仍然存在

1. **重启服务**:
   ```bash
   ./start.sh
   ```

2. **清除浏览器缓存**:
   - 按 Ctrl+Shift+R 强制刷新
   - 或清除浏览器缓存

3. **检查端口占用**:
   ```bash
   lsof -i :8080
   lsof -i :8000
   ```

4. **查看服务日志**:
   - 前端: 查看终端输出
   - 后端: 查看Django服务器日志

## 📞 获取帮助

如果以上步骤都无法解决问题，请提供：
1. 浏览器控制台的错误信息
2. 网络请求的详细信息
3. 后端服务器的日志输出 