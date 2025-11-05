# -*- coding: utf-8 -*-
"""
主API服务
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional

from config import API_TITLE, API_DESCRIPTION, API_VERSION
from models import IssueCreate, Issue, IssueListResponse, ExportRequest
from storage import storage
from excel_exporter import exporter

# 创建FastAPI应用
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["首页"])
async def root():
    """欢迎页面"""
    return {
        "message": "欢迎使用问题反馈跟踪系统API",
        "docs": "/docs",
        "version": API_VERSION
    }


@app.post("/api/issues", response_model=Issue, tags=["问题管理"])
async def create_issue(issue: IssueCreate):
    """创建新的问题记录"""
    try:
        created_issue = storage.create_issue(issue)
        return created_issue
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建问题失败: {str(e)}")


@app.get("/api/issues", response_model=IssueListResponse, tags=["问题管理"])
async def get_issues(
    date: Optional[str] = Query(None, description="筛选指定日期的问题 (格式: YYYY-MM-DD)"),
    start_date: Optional[str] = Query(None, description="开始日期 (格式: YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (格式: YYYY-MM-DD)"),
):
    """获取问题列表"""
    try:
        if date:
            issues = storage.get_issues_by_date(date)
        elif start_date and end_date:
            issues = storage.get_issues_by_date_range(start_date, end_date)
        elif start_date or end_date:
            raise HTTPException(status_code=400, detail="start_date和end_date必须同时提供")
        else:
            issues = storage.get_all_issues()
        
        return IssueListResponse(total=len(issues), issues=issues)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问题列表失败: {str(e)}")


@app.get("/api/issues/{issue_id}", response_model=Issue, tags=["问题管理"])
async def get_issue(issue_id: str):
    """根据ID获取问题详情"""
    issue = storage.get_issue_by_id(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="问题不存在")
    return issue


@app.delete("/api/issues/{issue_id}", tags=["问题管理"])
async def delete_issue(issue_id: str):
    """删除问题"""
    success = storage.delete_issue(issue_id)
    if not success:
        raise HTTPException(status_code=404, detail="问题不存在")
    return {"message": "删除成功", "issue_id": issue_id}


@app.get("/api/stats", tags=["统计"])
async def get_stats():
    """获取统计信息"""
    try:
        stats = storage.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


@app.post("/api/export", tags=["导出"])
async def export_issues(export_req: ExportRequest = None):
    """导出问题到Excel文件"""
    try:
        if export_req is None:
            export_req = ExportRequest()
        
        if export_req.date:
            issues = storage.get_issues_by_date(export_req.date)
            filename_suffix = export_req.date
        elif export_req.start_date and export_req.end_date:
            issues = storage.get_issues_by_date_range(export_req.start_date, export_req.end_date)
            filename_suffix = f"{export_req.start_date}_至_{export_req.end_date}"
        elif export_req.start_date or export_req.end_date:
            raise HTTPException(status_code=400, detail="start_date和end_date必须同时提供")
        else:
            issues = storage.get_all_issues()
            filename_suffix = "全部"
        
        if not issues:
            raise HTTPException(status_code=404, detail="没有找到符合条件的问题")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"问题跟进记录_{filename_suffix}_{timestamp}.xlsx"
        
        filepath = exporter.export_issues(issues, filename)
        
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@app.get("/api/export", tags=["导出"])
async def export_issues_get(
    date: Optional[str] = Query(None, description="导出指定日期的问题 (格式: YYYY-MM-DD)"),
    start_date: Optional[str] = Query(None, description="开始日期 (格式: YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (格式: YYYY-MM-DD)"),
):
    """导出问题到Excel文件（GET方式）"""
    export_req = ExportRequest(date=date, start_date=start_date, end_date=end_date)
    return await export_issues(export_req)


if __name__ == "__main__":
    import uvicorn
    from config import HOST, PORT
    
    print(f"启动服务器: http://{HOST}:{PORT}")
    print(f"API文档: http://{HOST}:{PORT}/docs")
    
    uvicorn.run(app, host=HOST, port=PORT)
