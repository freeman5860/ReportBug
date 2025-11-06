# -*- coding: utf-8 -*-
"""
数据模型定义
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IssueCreate(BaseModel):
    """创建问题的请求模型"""
    description: str = Field(..., description="问题描述", min_length=1)
    reporter: Optional[str] = Field(None, description="反馈人")
    created_at: Optional[str] = Field(None, description="问题创建时间 (格式: YYYY-MM-DD HH:MM:SS)")
    status: Optional[str] = Field(None, description="问题状态")
    priority: Optional[str] = Field(None, description="优先级")
    remarks: Optional[str] = Field(None, description="备注")

    class Config:
        json_schema_extra = {
            "example": {
                "description": "IM消息发送失败",
                "reporter": "张三",
                "created_at": "2025-11-05 14:30:00",
                "status": "待处理",
                "priority": "高",
                "remarks": "偶现问题"
            }
        }


class Issue(BaseModel):
    """问题完整模型"""
    id: str = Field(..., description="问题唯一ID")
    description: str = Field(..., description="问题描述")
    reporter: str = Field(..., description="反馈人")
    created_at: str = Field(..., description="问题创建时间")
    status: str = Field(..., description="问题状态")
    priority: str = Field(..., description="优先级")
    remarks: str = Field(..., description="备注")
    recorded_at: str = Field(..., description="记录时间（系统生成）")


class IssueListResponse(BaseModel):
    """问题列表响应"""
    total: int = Field(..., description="总数")
    issues: list[Issue] = Field(..., description="问题列表")


class ExportRequest(BaseModel):
    """导出请求模型"""
    date: Optional[str] = Field(None, description="导出指定日期的记录 (格式: YYYY-MM-DD)")
    start_date: Optional[str] = Field(None, description="开始日期 (格式: YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="结束日期 (格式: YYYY-MM-DD)")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-11-05"
            }
        }
