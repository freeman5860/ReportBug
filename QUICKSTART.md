# ⚡ 快速启动指南

5分钟快速上手问题反馈跟踪系统！

## 🎯 本地开发

### 1. 安装依赖（30秒）

```bash
cd ReportBug
pip install -r requirements.txt
```

### 2. 启动服务（5秒）

```bash
python main.py
```

看到以下输出说明启动成功：
```
启动服务器: http://0.0.0.0:8000
API文档: http://0.0.0.0:8000/docs
```

### 3. 访问API文档

打开浏览器访问：**http://localhost:8000/docs**

你会看到一个漂亮的交互式API文档界面（Swagger UI）

### 4. 测试API（可选）

运行测试脚本：

```bash
python test_api.py
```

## 🌐 快速部署到Railway

### 步骤1：推送到GitHub（1分钟）

```bash
# 初始化git
git init
git add .
git commit -m "Initial commit"

# 推送到GitHub（需要先创建GitHub仓库）
git remote add origin https://github.com/你的用户名/ReportBug.git
git branch -M main
git push -u origin main
```

### 步骤2：部署到Railway（3分钟）

1. 访问 https://railway.app
2. 用GitHub登录
3. 点击 **New Project** → **Deploy from GitHub repo**
4. 选择你的 `ReportBug` 仓库
5. 等待自动部署完成（1-2分钟）
6. 点击项目 → **Settings** → **Networking** → **Generate Domain**
7. 获得你的API地址：`https://your-app.railway.app`

完成！访问 `https://your-app.railway.app/docs` 查看你的API

## 📱 使用API

### 方式1：浏览器（最简单）

访问 `http://localhost:8000/docs`，在Swagger界面直接测试

### 方式2：cURL

```bash
# 创建问题
curl -X POST "http://localhost:8000/api/issues" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "测试问题",
    "reporter": "张三"
  }'

# 查询问题
curl "http://localhost:8000/api/issues"

# 导出Excel（下载到当前目录）
curl -O "http://localhost:8000/api/export"
```

### 方式3：Python

```python
import requests

# 创建问题
response = requests.post("http://localhost:8000/api/issues", json={
    "description": "登录失败",
    "reporter": "李四",
    "priority": "高"
})
print(response.json())

# 查询问题
response = requests.get("http://localhost:8000/api/issues")
print(response.json())

# 导出Excel
response = requests.get("http://localhost:8000/api/export")
with open("问题记录.xlsx", "wb") as f:
    f.write(response.content)
```

### 方式4：使用测试脚本

```bash
python test_api.py
```

会自动创建测试数据并导出Excel

## 🎨 API功能一览

| 功能 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 创建问题 | POST | `/api/issues` | 提交新问题 |
| 查询问题 | GET | `/api/issues` | 获取问题列表 |
| 问题详情 | GET | `/api/issues/{id}` | 查看单个问题 |
| 删除问题 | DELETE | `/api/issues/{id}` | 删除指定问题 |
| 统计信息 | GET | `/api/stats` | 获取统计数据 |
| 导出Excel | GET | `/api/export` | 下载Excel文件 |

## 📝 问题字段说明

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| description | ✅ | - | 问题描述 |
| reporter | ✅ | - | 反馈人 |
| created_at | ❌ | 当前时间 | 问题创建时间 |
| status | ❌ | 待处理 | 问题状态 |
| priority | ❌ | 中 | 优先级（高/中/低） |
| category | ❌ | 其他 | 问题分类 |
| remarks | ❌ | 空 | 备注 |

## 🎯 常用操作

### 导出今天的问题

```bash
# 浏览器直接访问
http://localhost:8000/api/export?date=2025-11-05

# 或使用curl
curl -O "http://localhost:8000/api/export?date=2025-11-05"
```

### 导出日期范围

```bash
curl -O "http://localhost:8000/api/export?start_date=2025-11-01&end_date=2025-11-05"
```

### 查询今天的问题

```bash
curl "http://localhost:8000/api/issues?date=2025-11-05"
```

## 🐳 Docker运行（可选）

```bash
# 构建并运行
docker build -t report-bug-api .
docker run -d -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/exports:/app/exports \
  report-bug-api

# 访问API
open http://localhost:8000/docs
```

## 🔧 故障排查

### 端口被占用

```bash
# 修改端口
PORT=8080 python main.py
```

### 缺少依赖

```bash
pip install -r requirements.txt --upgrade
```

### 权限问题

```bash
# 确保有写入权限
chmod 755 data exports
```

## 📚 更多信息

- 详细文档：`README.md`
- 部署指南：`DEPLOYMENT.md`
- 在线API文档：`http://localhost:8000/docs`
- 备用API文档：`http://localhost:8000/redoc`

## 🆘 需要帮助？

1. 查看完整文档：`README.md`
2. 查看API文档：http://localhost:8000/docs
3. 提交Issue到GitHub

---

**开始使用吧！** 🚀

