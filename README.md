# 问题反馈跟踪系统 API

一个简单高效的问题反馈记录和导出系统。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python main.py
```

### 3. 访问API文档

打开浏览器访问：http://localhost:8000/docs

### 4. 测试API

```bash
python test_api.py
```

## 功能特性

- 📝 记录问题信息
- 🔍 按日期查询问题
- 📊 统计分析
- 📥 导出Excel文件
- 💾 JSON文件存储

## API接口

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/issues` | POST | 创建问题 |
| `/api/issues` | GET | 查询问题 |
| `/api/issues/{id}` | GET | 获取问题详情 |
| `/api/issues/{id}` | DELETE | 删除问题 |
| `/api/stats` | GET | 统计信息 |
| `/api/export` | GET/POST | 导出Excel |

## 使用示例

### 创建问题

```bash
curl -X POST "http://localhost:8000/api/issues" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "测试问题",
    "reporter": "张三",
    "priority": "高"
  }'
```

### 查询问题

```bash
curl "http://localhost:8000/api/issues?date=2025-11-05"
```

### 导出Excel

```bash
curl -O "http://localhost:8000/api/export"
```

## 部署到Railway

1. 推送代码到GitHub
2. 访问 https://railway.app
3. 连接GitHub仓库
4. 自动部署完成

## 许可证

MIT License
