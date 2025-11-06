# 问题反馈跟踪系统 API 文档

## 概述

本文档描述了问题反馈跟踪系统的 RESTful API 接口，适用于 iOS 应用开发。

**API 版本**: 1.0.0  
**Base URL**: `https://reportbug-production.up.railway.app` (请替换为你的实际部署地址)

> 💡 **提示**: 所有接口都支持 CORS，可以直接从 iOS 应用调用。

---

## 目录

- [数据模型](#数据模型)
- [接口列表](#接口列表)
  - [1. 首页](#1-首页)
  - [2. 创建问题](#2-创建问题)
  - [3. 获取问题列表](#3-获取问题列表)
  - [4. 获取问题详情](#4-获取问题详情)
  - [5. 删除问题](#5-删除问题)
  - [6. 获取统计信息](#6-获取统计信息)
  - [7. 导出问题](#7-导出问题)
- [错误处理](#错误处理)
- [iOS 调用示例](#ios-调用示例)

---

## 数据模型

### IssueCreate (创建问题请求)

```json
{
  "description": "string (必填, 问题描述)",
  "reporter": "string (可选, 反馈人)",
  "created_at": "string (可选, 格式: YYYY-MM-DD HH:MM:SS)",
  "status": "string (可选, 默认: 待处理)",
  "priority": "string (可选, 默认: 中, 可选值: 高/中/低)",
  "remarks": "string (可选, 备注)"
}
```

### Issue (问题完整信息)

```json
{
  "id": "string (唯一ID, UUID格式)",
  "description": "string (问题描述)",
  "reporter": "string (反馈人)",
  "created_at": "string (问题创建时间, 格式: YYYY-MM-DD HH:MM:SS)",
  "status": "string (问题状态)",
  "priority": "string (优先级)",
  "remarks": "string (备注)",
  "recorded_at": "string (记录时间, 系统生成)"
}
```

### IssueListResponse (问题列表响应)

```json
{
  "total": 0,
  "issues": [
    {
      // Issue 对象数组
    }
  ]
}
```

### StatsResponse (统计信息响应)

```json
{
  "total": 0,
  "by_status": {
    "待处理": 5,
    "处理中": 3,
    "已解决": 10
  },
  "by_priority": {
    "高": 2,
    "中": 10,
    "低": 6
  }
}
```

---

## 接口列表

### 1. 首页

获取 API 基本信息。

**请求**

```
GET /
```

**响应**

```json
{
  "message": "欢迎使用问题反馈跟踪系统API",
  "docs": "/docs",
  "version": "1.0.0"
}
```

**状态码**: `200 OK`

---

### 2. 创建问题

创建新的问题记录。

**请求**

```
POST /api/issues
Content-Type: application/json
```

**请求体**

```json
{
  "description": "IM消息发送失败",
  "reporter": "张三",
  "created_at": "2025-11-05 14:30:00",
  "status": "待处理",
  "priority": "高",
  "remarks": "偶现问题"
}
```

**必填字段**: `description`  
**可选字段**: `reporter`, `created_at`, `status`, `priority`, `remarks`

**响应**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "IM消息发送失败",
  "reporter": "张三",
  "created_at": "2025-11-05 14:30:00",
  "status": "待处理",
  "priority": "高",
  "remarks": "偶现问题",
  "recorded_at": "2025-11-05 15:00:00"
}
```

**状态码**: `200 OK`

**错误响应**

```json
{
  "detail": "创建问题失败: [错误信息]"
}
```

**状态码**: `500 Internal Server Error`

---

### 3. 获取问题列表

获取问题列表，支持按日期筛选。

**请求**

```
GET /api/issues?date=2025-11-05
GET /api/issues?start_date=2025-11-01&end_date=2025-11-30
GET /api/issues
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `date` | string | 否 | 筛选指定日期的问题 (格式: YYYY-MM-DD) |
| `start_date` | string | 否 | 开始日期 (格式: YYYY-MM-DD)，必须与 `end_date` 同时使用 |
| `end_date` | string | 否 | 结束日期 (格式: YYYY-MM-DD)，必须与 `start_date` 同时使用 |

**响应**

```json
{
  "total": 2,
  "issues": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "description": "IM消息发送失败",
      "reporter": "张三",
      "created_at": "2025-11-05 14:30:00",
      "status": "待处理",
      "priority": "高",
      "remarks": "偶现问题",
      "recorded_at": "2025-11-05 15:00:00"
    }
  ]
}
```

**状态码**: `200 OK`

**错误响应**

```json
{
  "detail": "start_date和end_date必须同时提供"
}
```

**状态码**: `400 Bad Request`

---

### 4. 获取问题详情

根据问题 ID 获取详细信息。

**请求**

```
GET /api/issues/{issue_id}
```

**路径参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `issue_id` | string | 问题的唯一ID (UUID格式) |

**响应**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "IM消息发送失败",
  "reporter": "张三",
  "created_at": "2025-11-05 14:30:00",
  "status": "待处理",
  "priority": "高",
  "remarks": "偶现问题",
  "recorded_at": "2025-11-05 15:00:00"
}
```

**状态码**: `200 OK`

**错误响应**

```json
{
  "detail": "问题不存在"
}
```

**状态码**: `404 Not Found`

---

### 5. 删除问题

删除指定问题。

**请求**

```
DELETE /api/issues/{issue_id}
```

**路径参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `issue_id` | string | 问题的唯一ID (UUID格式) |

**响应**

```json
{
  "message": "删除成功",
  "issue_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**状态码**: `200 OK`

**错误响应**

```json
{
  "detail": "问题不存在"
}
```

**状态码**: `404 Not Found`

---

### 6. 获取统计信息

获取问题的统计信息，包括总数、按状态/优先级/分类的统计。

**请求**

```
GET /api/stats
```

**响应**

```json
{
  "total": 18,
  "by_status": {
    "待处理": 5,
    "处理中": 3,
    "已解决": 10
  },
  "by_priority": {
    "高": 2,
    "中": 10,
    "低": 6
  }
}
```

**状态码**: `200 OK`

**错误响应**

```json
{
  "detail": "获取统计信息失败: [错误信息]"
}
```

**状态码**: `500 Internal Server Error`

---

### 7. 导出问题

导出问题到 Excel 文件，支持按日期筛选。

**请求**

```
GET /api/export?date=2025-11-05
GET /api/export?start_date=2025-11-01&end_date=2025-11-30
GET /api/export
```

**或使用 POST 方式**

```
POST /api/export
Content-Type: application/json
```

**POST 请求体**

```json
{
  "date": "2025-11-05"
}
```

或

```json
{
  "start_date": "2025-11-01",
  "end_date": "2025-11-30"
}
```

**查询参数 (GET 方式)**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `date` | string | 否 | 导出指定日期的问题 (格式: YYYY-MM-DD) |
| `start_date` | string | 否 | 开始日期 (格式: YYYY-MM-DD)，必须与 `end_date` 同时使用 |
| `end_date` | string | 否 | 结束日期 (格式: YYYY-MM-DD)，必须与 `start_date` 同时使用 |

**响应**

返回 Excel 文件 (.xlsx)，文件名格式：`问题跟进记录_{日期范围}_{时间戳}.xlsx`

**Content-Type**: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

**状态码**: `200 OK`

**错误响应**

```json
{
  "detail": "没有找到符合条件的问题"
}
```

**状态码**: `404 Not Found`

```json
{
  "detail": "start_date和end_date必须同时提供"
}
```

**状态码**: `400 Bad Request`

---

## 错误处理

### 标准错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "detail": "错误描述信息"
}
```

### 常见 HTTP 状态码

| 状态码 | 说明 | 示例场景 |
|--------|------|----------|
| `200` | 成功 | 请求成功处理 |
| `400` | 请求参数错误 | 缺少必需参数、参数格式错误 |
| `404` | 资源不存在 | 问题ID不存在、没有符合条件的数据 |
| `500` | 服务器内部错误 | 数据库错误、系统异常 |

---

## iOS 调用示例

### 基础配置

首先，创建一个 API 管理器类：

```swift
import Foundation

class IssueAPIManager {
    static let shared = IssueAPIManager()
    
    // 替换为你的实际部署地址
    private let baseURL = "https://reportbug-production.up.railway.app"
    
    private init() {}
    
    // 通用请求方法
    private func request<T: Decodable>(
        url: URL,
        method: String,
        body: Data? = nil
    ) async throws -> T {
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let body = body {
            request.httpBody = body
        }
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        
        guard (200...299).contains(httpResponse.statusCode) else {
            let errorMessage = try? JSONDecoder().decode(ErrorResponse.self, from: data)
            throw APIError.serverError(message: errorMessage?.detail ?? "未知错误")
        }
        
        let decoder = JSONDecoder()
        return try decoder.decode(T.self, from: data)
    }
}

// 错误类型
enum APIError: Error {
    case invalidURL
    case invalidResponse
    case serverError(message: String)
}

// 错误响应模型
struct ErrorResponse: Codable {
    let detail: String
}
```

### 数据模型

```swift
// MARK: - 请求模型
struct IssueCreate: Codable {
    let description: String
    let reporter: String?
    let createdAt: String?
    let status: String?
    let priority: String?
    let remarks: String?
    
    enum CodingKeys: String, CodingKey {
        case description
        case reporter
        case createdAt = "created_at"
        case status
        case priority
        case remarks
    }
}

// MARK: - 响应模型
struct Issue: Codable, Identifiable {
    let id: String
    let description: String
    let reporter: String
    let createdAt: String
    let status: String
    let priority: String
    let remarks: String
    let recordedAt: String
    
    enum CodingKeys: String, CodingKey {
        case id
        case description
        case reporter
        case createdAt = "created_at"
        case status
        case priority
        case remarks
        case recordedAt = "recorded_at"
    }
}

struct IssueListResponse: Codable {
    let total: Int
    let issues: [Issue]
}

struct StatsResponse: Codable {
    let total: Int
    let byStatus: [String: Int]
    let byPriority: [String: Int]
    
    enum CodingKeys: String, CodingKey {
        case total
        case byStatus = "by_status"
        case byPriority = "by_priority"
    }
}
```

### API 方法实现

在 `IssueAPIManager` 中添加具体方法：

```swift
extension IssueAPIManager {
    // MARK: - 创建问题
    func createIssue(_ issue: IssueCreate) async throws -> Issue {
        guard let url = URL(string: "\(baseURL)/api/issues") else {
            throw APIError.invalidURL
        }
        
        let encoder = JSONEncoder()
        let body = try encoder.encode(issue)
        
        return try await request(url: url, method: "POST", body: body)
    }
    
    // MARK: - 获取问题列表
    func getIssues(
        date: String? = nil,
        startDate: String? = nil,
        endDate: String? = nil
    ) async throws -> IssueListResponse {
        var components = URLComponents(string: "\(baseURL)/api/issues")
        
        var queryItems: [URLQueryItem] = []
        if let date = date {
            queryItems.append(URLQueryItem(name: "date", value: date))
        }
        if let startDate = startDate {
            queryItems.append(URLQueryItem(name: "start_date", value: startDate))
        }
        if let endDate = endDate {
            queryItems.append(URLQueryItem(name: "end_date", value: endDate))
        }
        
        if !queryItems.isEmpty {
            components?.queryItems = queryItems
        }
        
        guard let url = components?.url else {
            throw APIError.invalidURL
        }
        
        return try await request(url: url, method: "GET")
    }
    
    // MARK: - 获取问题详情
    func getIssue(id: String) async throws -> Issue {
        guard let url = URL(string: "\(baseURL)/api/issues/\(id)") else {
            throw APIError.invalidURL
        }
        
        return try await request(url: url, method: "GET")
    }
    
    // MARK: - 删除问题
    func deleteIssue(id: String) async throws -> DeleteResponse {
        guard let url = URL(string: "\(baseURL)/api/issues/\(id)") else {
            throw APIError.invalidURL
        }
        
        return try await request(url: url, method: "DELETE")
    }
    
    // MARK: - 获取统计信息
    func getStats() async throws -> StatsResponse {
        guard let url = URL(string: "\(baseURL)/api/stats") else {
            throw APIError.invalidURL
        }
        
        return try await request(url: url, method: "GET")
    }
    
    // MARK: - 导出问题
    func exportIssues(
        date: String? = nil,
        startDate: String? = nil,
        endDate: String? = nil
    ) async throws -> Data {
        var components = URLComponents(string: "\(baseURL)/api/export")
        
        var queryItems: [URLQueryItem] = []
        if let date = date {
            queryItems.append(URLQueryItem(name: "date", value: date))
        }
        if let startDate = startDate {
            queryItems.append(URLQueryItem(name: "start_date", value: startDate))
        }
        if let endDate = endDate {
            queryItems.append(URLQueryItem(name: "end_date", value: endDate))
        }
        
        if !queryItems.isEmpty {
            components?.queryItems = queryItems
        }
        
        guard let url = components?.url else {
            throw APIError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.serverError(message: "导出失败")
        }
        
        return data
    }
}

struct DeleteResponse: Codable {
    let message: String
    let issueId: String
    
    enum CodingKeys: String, CodingKey {
        case message
        case issueId = "issue_id"
    }
}
```

### 使用示例

```swift
// MARK: - 创建问题
Task {
    do {
        let newIssue = IssueCreate(
            description: "IM消息发送失败",
            reporter: "张三",
            createdAt: nil,
            status: "待处理",
            priority: "高",
            remarks: "偶现问题"
        )
        
        let createdIssue = try await IssueAPIManager.shared.createIssue(newIssue)
        print("创建成功: \(createdIssue.id)")
    } catch {
        print("创建失败: \(error)")
    }
}

// MARK: - 获取所有问题
Task {
    do {
        let response = try await IssueAPIManager.shared.getIssues()
        print("共 \(response.total) 条问题")
        for issue in response.issues {
            print("\(issue.description) - \(issue.reporter)")
        }
    } catch {
        print("获取失败: \(error)")
    }
}

// MARK: - 按日期筛选
Task {
    do {
        let response = try await IssueAPIManager.shared.getIssues(date: "2025-11-05")
        print("今日共 \(response.total) 条问题")
    } catch {
        print("获取失败: \(error)")
    }
}

// MARK: - 获取统计信息
Task {
    do {
        let stats = try await IssueAPIManager.shared.getStats()
        print("总计: \(stats.total)")
        print("按状态: \(stats.byStatus)")
        print("按优先级: \(stats.byPriority)")
    } catch {
        print("获取失败: \(error)")
    }
}

// MARK: - 导出问题
Task {
    do {
        let excelData = try await IssueAPIManager.shared.exportIssues(
            startDate: "2025-11-01",
            endDate: "2025-11-30"
        )
        
        // 保存到文件
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let fileURL = documentsPath.appendingPathComponent("问题跟进记录.xlsx")
        try excelData.write(to: fileURL)
        
        print("导出成功: \(fileURL)")
    } catch {
        print("导出失败: \(error)")
    }
}
```

### 日期格式化工具

```swift
extension DateFormatter {
    static let apiDateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter
    }()
    
    static let apiDateTimeFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        return formatter
    }()
}

// 使用示例
let dateString = DateFormatter.apiDateFormatter.string(from: Date())
// 输出: "2025-11-05"
```

---

## 注意事项

1. **Base URL**: 请将代码中的 `baseURL` 替换为你实际部署在 Railway 的应用地址。

2. **日期格式**: 
   - 日期格式必须为 `YYYY-MM-DD`（如：`2025-11-05`）
   - 日期时间格式必须为 `YYYY-MM-DD HH:MM:SS`（如：`2025-11-05 14:30:00`）

3. **错误处理**: 建议在实际应用中实现完整的错误处理逻辑，包括网络错误、超时等。

4. **异步调用**: 所有 API 调用都是异步的，使用 `async/await` 语法。

5. **文件下载**: 导出接口返回的是 Excel 文件二进制数据，需要保存到本地文件系统。

6. **CORS**: API 已配置 CORS，允许所有来源访问，无需特殊配置。

---

## 测试

可以使用以下工具测试 API：

- **Swagger UI**: 访问 `https://reportbug-production.up.railway.app/docs`
- **Postman**: 导入上述接口进行测试
- **curl**: 命令行测试工具

示例 curl 命令：

```bash
# 创建问题
curl -X POST "https://reportbug-production.up.railway.app/api/issues" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "测试问题",
    "reporter": "测试用户",
    "priority": "高"
  }'

# 获取问题列表
curl "https://reportbug-production.up.railway.app/api/issues"

# 获取统计信息
curl "https://reportbug-production.up.railway.app/api/stats"
```

---

**文档版本**: 1.0.0  
**最后更新**: 2025-11-05

