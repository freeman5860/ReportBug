# -*- coding: utf-8 -*-
"""
API测试脚本
"""
import requests
from datetime import datetime, date

BASE_URL = "http://localhost:8000"


def test_create_issue():
    """测试创建问题"""
    print("\n📝 测试创建问题...")
    
    issues = [
        {
            "description": "IM消息发送失败，点击发送后无响应",
            "reporter": "张三",
            "priority": "高",
            "category": "功能bug",
            "remarks": "仅在WiFi网络下出现"
        },
        {
            "description": "首页加载速度慢，需要5-10秒",
            "reporter": "李四",
            "priority": "中",
            "category": "性能问题",
            "status": "处理中"
        },
        {
            "description": "个人资料页面头像显示错误",
            "reporter": "王五",
            "priority": "低",
            "category": "UI问题",
        }
    ]
    
    created_ids = []
    for issue in issues:
        response = requests.post(f"{BASE_URL}/api/issues", json=issue)
        if response.status_code == 200:
            data = response.json()
            created_ids.append(data['id'])
            print(f"✅ 创建成功: {issue['description'][:20]}... (ID: {data['id'][:8]}...)")
        else:
            print(f"❌ 创建失败: {response.text}")
    
    return created_ids


def test_get_issues():
    """测试查询问题"""
    print("\n🔍 测试查询所有问题...")
    
    response = requests.get(f"{BASE_URL}/api/issues")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 查询成功: 共 {data['total']} 条记录")
        for issue in data['issues'][:3]:
            print(f"   - {issue['description'][:30]}... | {issue['reporter']} | {issue['status']}")
    else:
        print(f"❌ 查询失败: {response.text}")


def test_get_issues_by_date():
    """测试按日期查询"""
    print("\n📅 测试按日期查询...")
    
    today = date.today().strftime("%Y-%m-%d")
    response = requests.get(f"{BASE_URL}/api/issues", params={"date": today})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 查询成功: {today} 共 {data['total']} 条记录")
    else:
        print(f"❌ 查询失败: {response.text}")


def test_get_stats():
    """测试统计信息"""
    print("\n📊 测试获取统计信息...")
    
    response = requests.get(f"{BASE_URL}/api/stats")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 统计成功:")
        print(f"   总数: {data['total']}")
        print(f"   按状态: {data['by_status']}")
        print(f"   按优先级: {data['by_priority']}")
        print(f"   按分类: {data['by_category']}")
    else:
        print(f"❌ 统计失败: {response.text}")


def test_export():
    """测试导出Excel"""
    print("\n📥 测试导出Excel...")
    
    response = requests.get(f"{BASE_URL}/api/export")
    if response.status_code == 200:
        filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ 导出成功: {filename}")
    else:
        print(f"❌ 导出失败: {response.text}")


def test_delete_issue(issue_id):
    """测试删除问题"""
    print(f"\n🗑️  测试删除问题 {issue_id[:8]}...")
    
    response = requests.delete(f"{BASE_URL}/api/issues/{issue_id}")
    if response.status_code == 200:
        print(f"✅ 删除成功")
    else:
        print(f"❌ 删除失败: {response.text}")


def main():
    print("=" * 60)
    print("🚀 开始测试问题反馈跟踪系统API")
    print("=" * 60)
    
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("❌ 服务未运行，请先启动服务：python main.py")
            return
        
        print("✅ 服务正常运行")
        
        created_ids = test_create_issue()
        test_get_issues()
        test_get_issues_by_date()
        test_get_stats()
        test_export()
        
        if created_ids:
            test_delete_issue(created_ids[0])
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务，请确保服务正在运行：python main.py")
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")


if __name__ == "__main__":
    main()
