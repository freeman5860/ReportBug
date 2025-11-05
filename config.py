# -*- coding: utf-8 -*-
"""
配置文件
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 数据存储目录
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 导出文件目录
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True)

# JSON数据文件路径
ISSUES_FILE = DATA_DIR / "issues.json"

# API配置
API_TITLE = "问题反馈跟踪系统"
API_DESCRIPTION = "用于记录和导出问题反馈的API服务"
API_VERSION = "1.0.0"

# 服务器配置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
