# 🚀 部署指南

本文档详细说明如何将问题反馈跟踪系统部署到各种平台。

## 📋 目录

1. [Railway部署](#railway部署) ⭐ 推荐
2. [Render部署](#render部署)
3. [Fly.io部署](#flyio部署)
4. [Docker部署](#docker部署)
5. [传统服务器部署](#传统服务器部署)

---

## Railway部署 ⭐

Railway是最简单快速的部署方式，免费且功能强大。

### 前置要求

- GitHub账号
- 项目已推送到GitHub

### 步骤

#### 1. 推送代码到GitHub

```bash
# 初始化git仓库
cd ReportBug
git init

# 添加所有文件
git add .
git commit -m "Initial commit"

# 创建GitHub仓库后，添加远程仓库
git remote add origin https://github.com/your-username/ReportBug.git
git branch -M main
git push -u origin main
```

#### 2. 在Railway创建项目

1. 访问 [Railway.app](https://railway.app)
2. 点击 **"Start a New Project"**
3. 选择 **"Deploy from GitHub repo"**
4. 授权Railway访问你的GitHub
5. 选择 `ReportBug` 仓库

#### 3. 等待部署

- Railway会自动检测Python项目
- 自动安装 `requirements.txt` 中的依赖
- 使用 `railway.toml` 中的启动命令
- 约1-2分钟完成部署

#### 4. 获取访问地址

1. 在Railway项目页面
2. 点击 **Settings** → **Networking**
3. 点击 **Generate Domain**
4. 获得类似 `your-app.railway.app` 的地址

#### 5. 访问你的API

```bash
https://your-app.railway.app/docs
```

### Railway配置说明

Railway会自动设置以下环境变量：
- `PORT`: Railway自动分配的端口

无需额外配置！

### 数据持久化（重要）

⚠️ **注意**：Railway默认不持久化文件系统。每次重新部署后，`data/issues.json` 会被重置。

**解决方案：**

1. **使用Railway Volumes**（推荐）
   - 在项目设置中添加Volume
   - 挂载到 `/app/data` 目录

2. **定期备份**
   - 定期调用 `/api/export` 导出数据
   - 保存到本地或云存储

3. **使用外部数据库**
   - 升级到使用Redis或MongoDB
   - Railway提供数据库插件

---

## Render部署

Render提供免费tier，适合小型项目。

### 步骤

1. 访问 [Render.com](https://render.com)
2. 注册并登录
3. 点击 **New** → **Web Service**
4. 连接GitHub仓库
5. 配置：
   - **Name**: report-bug-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. 点击 **Create Web Service**

### 注意事项

- 免费tier会在15分钟无活动后休眠
- 首次请求需要等待服务唤醒（约30秒）
- 同样需要考虑数据持久化问题

---

## Fly.io部署

Fly.io提供全球分布式部署，性能优秀。

### 前置要求

- 安装 [flyctl](https://fly.io/docs/hands-on/install-flyctl/)
- Fly.io账号（需要信用卡验证）

### 步骤

```bash
# 登录
flyctl auth login

# 初始化项目
flyctl launch

# 按照提示配置：
# - 应用名称
# - 地区选择
# - 不添加数据库（我们用JSON）

# 部署
flyctl deploy

# 查看状态
flyctl status

# 访问应用
flyctl open
```

### Fly.io配置

`fly.toml` 文件会自动生成，确保包含：

```toml
[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

---

## Docker部署

适合在任意支持Docker的环境部署。

### 本地Docker运行

```bash
# 构建镜像
docker build -t report-bug-api .

# 运行容器（带数据持久化）
docker run -d \
  --name report-bug-api \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/exports:/app/exports \
  report-bug-api

# 查看日志
docker logs -f report-bug-api

# 停止容器
docker stop report-bug-api

# 删除容器
docker rm report-bug-api
```

### Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./exports:/app/exports
    restart: unless-stopped
```

运行：

```bash
docker-compose up -d
```

---

## 传统服务器部署

适合阿里云、腾讯云等传统VPS。

### 1. 安装Python环境

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS
sudo yum install python3 python3-pip
```

### 2. 部署应用

```bash
# 克隆代码
git clone <your-repo-url>
cd ReportBug

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 测试运行
python main.py
```

### 3. 使用Systemd管理服务

创建 `/etc/systemd/system/report-bug.service`:

```ini
[Unit]
Description=Report Bug API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/ReportBug
Environment="PATH=/path/to/ReportBug/venv/bin"
ExecStart=/path/to/ReportBug/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable report-bug
sudo systemctl start report-bug
sudo systemctl status report-bug
```

### 4. 配置Nginx反向代理

创建 `/etc/nginx/sites-available/report-bug`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/report-bug /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. 配置HTTPS（可选）

使用Let's Encrypt：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 📊 部署方案对比

| 平台 | 难度 | 免费额度 | 启动速度 | 持久化 | 推荐度 |
|------|------|----------|----------|--------|--------|
| Railway | ⭐ | 500h/月 | 快 | 需配置 | ⭐⭐⭐⭐⭐ |
| Render | ⭐⭐ | 750h/月 | 慢（冷启动） | 需配置 | ⭐⭐⭐⭐ |
| Fly.io | ⭐⭐⭐ | 3个实例 | 快 | 支持 | ⭐⭐⭐⭐ |
| Docker | ⭐⭐ | 自己负责 | 快 | 完全支持 | ⭐⭐⭐⭐ |
| VPS | ⭐⭐⭐⭐ | 需付费 | 快 | 完全支持 | ⭐⭐⭐ |

---

## 🔧 环境变量配置

所有平台都可以通过环境变量配置：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PORT` | 服务端口 | 8000 |
| `HOST` | 监听地址 | 0.0.0.0 |

在Railway/Render中设置环境变量：
1. 进入项目设置
2. 找到 Environment Variables
3. 添加变量

---

## 🚨 常见问题

### 1. 部署后无法访问

- 检查防火墙设置
- 确认端口配置正确
- 查看服务日志

### 2. 数据丢失

- 配置Volume或持久化存储
- 定期备份数据
- 考虑使用数据库

### 3. 服务崩溃

- 查看日志：`docker logs` 或平台日志
- 检查依赖是否安装完整
- 确认Python版本兼容

### 4. 性能问题

- 使用 `gunicorn` 替代 `uvicorn`
- 增加worker数量
- 考虑使用Redis缓存

---

## 📞 需要帮助？

如遇到部署问题，请：
1. 查看平台文档
2. 提交GitHub Issue
3. 查看服务日志排查问题

祝部署成功！🎉

