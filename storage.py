# -*- coding: utf-8 -*-
"""
JSON存储模块
"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from models import Issue, IssueCreate
from config import ISSUES_FILE


class JSONStorage:
    """JSON文件存储管理器"""
    
    def __init__(self, file_path: Path = ISSUES_FILE):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """确保JSON文件存在"""
        if not self.file_path.exists():
            self._write_data([])
    
    def _read_data(self) -> List[dict]:
        """读取JSON数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
        except Exception as e:
            print(f"读取数据出错: {e}")
            return []
    
    def _write_data(self, data: List[dict]):
        """写入JSON数据"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"写入数据出错: {e}")
            raise
    
    def create_issue(self, issue_data: IssueCreate) -> Issue:
        """创建新问题记录"""
        issues = self._read_data()
        
        # 生成唯一ID
        issue_id = str(uuid.uuid4())
        
        # 获取当前时间
        recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 如果没有提供创建时间，使用当前时间
        created_at = issue_data.created_at or recorded_at
        
        # 构建问题对象
        issue = Issue(
            id=issue_id,
            description=issue_data.description,
            reporter=issue_data.reporter or "",
            created_at=created_at,
            status=issue_data.status or "待处理",
            priority=issue_data.priority or "中",
            remarks=issue_data.remarks or "",
            recorded_at=recorded_at
        )
        
        # 添加到列表
        issues.append(issue.model_dump())
        self._write_data(issues)
        
        return issue
    
    def get_all_issues(self) -> List[Issue]:
        """获取所有问题"""
        issues_data = self._read_data()
        return [Issue(**issue) for issue in issues_data]
    
    def get_issues_by_date(self, date_str: str) -> List[Issue]:
        """获取指定日期的问题"""
        all_issues = self.get_all_issues()
        return [
            issue for issue in all_issues
            if issue.created_at.startswith(date_str)
        ]
    
    def get_issues_by_date_range(self, start_date: str, end_date: str) -> List[Issue]:
        """获取日期范围内的问题"""
        all_issues = self.get_all_issues()
        return [
            issue for issue in all_issues
            if start_date <= issue.created_at[:10] <= end_date
        ]
    
    def get_issue_by_id(self, issue_id: str) -> Optional[Issue]:
        """根据ID获取问题"""
        issues = self.get_all_issues()
        for issue in issues:
            if issue.id == issue_id:
                return issue
        return None
    
    def delete_issue(self, issue_id: str) -> bool:
        """删除问题"""
        issues = self._read_data()
        original_length = len(issues)
        issues = [issue for issue in issues if issue['id'] != issue_id]
        
        if len(issues) < original_length:
            self._write_data(issues)
            return True
        return False
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        issues = self.get_all_issues()
        return {
            "total": len(issues),
            "by_status": self._count_by_field(issues, "status"),
            "by_priority": self._count_by_field(issues, "priority")
        }
    
    @staticmethod
    def _count_by_field(issues: List[Issue], field: str) -> dict:
        """按字段统计"""
        counts = {}
        for issue in issues:
            value = getattr(issue, field)
            counts[value] = counts.get(value, 0) + 1
        return counts


# 全局存储实例
storage = JSONStorage()
