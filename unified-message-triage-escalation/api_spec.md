# API Specification
Unified Smart Message Triage & Escalation System
> 后端接口文档，供前端对接，内部REST风格，无鉴权演示版本

## Base URL
`http://127.0.0.1:8000/api/v1`
Content-Type: `application/json`

---

### 消息与分析模块
#### POST `/messages/ingest`
**功能：** 接收来自WhatsApp / Email / Discord的标准化消息写入raw_messages
Request Body
```json
{
  "message_id":"MSG-XXXX",
  "platform":"whatsapp|email|discord",
  "original_message_id":"xxx",
  "sender_id":"C001",
  "platform_sender_id":"...",
  "sender_name":"Alya Tan",
  "sender_role":"customer",
  "project_id":"P001",
  "content":"...",
  "subject":"",
  "received_at":"2026‑10‑20T09:00:00+08:00",
  "direction":"inbound",
  "conversation_id":"...",
  "attachment_count":0,
  "ingestion_method":"synthetic_demo"
}



Response 200

```
{"ok":true,"message_id":"MSG‑XXXX"}
```

#### POST `/messages/analyze/{message_id}`

功能：执行单条消息 AI 打分、计算优先级、入任务队列
Response:

```
{
   "ok":true,
   "analysis":{
     "importance_score":14,
     "urgency_score":12,
     "computed_total_score":68,
     "assigned_tier":"P1",
     "risk_level":"high"
   }
}
```

---

### 任务队列接口（核心：下一项）

#### GET `/queue/next`

Query param: `agent_id=C001`
功能：获取下一条待处理任务（点击下一项） 返回最高优先级 pending 任务；无任务返回 `{"ok":true,"task":null}`

Response 200

```
{
   "ok": true,
   "task":{
     "task_id":1,
     "message_id":"MSG‑XXXX",
     "tier":"P1",
     "score":85,
     "status":"processing",
     "content":"...",
     "sender_name":"Alya Tan",
     "platform":"whatsapp",
     "due_sla_timestamp":"..."
   }
}
```

#### POST `/queue/task/{task_id}/complete`

完成任务 Body: `{"note":"handled issue"}`

#### POST `/queue/task/{task_id}/skip`

跳过任务 Body: `{"note":"skip this item"}`

#### POST `/queue/task/{task_id}/reassign`

改派任务 Body: `{"new_agent_id":"C002"}`

#### GET `/queue/summary`

获取队列统计，返回各 P1‑P4 待处理数量

---

### 超时升级 escalation 接口

#### GET `/escalation/check`

触发扫描全部任务 SLA 超时，自动升级；返回升级 task_id 列表

```
{"ok":true,"escalated_task_ids":[12,15]}
```

#### POST `/escalation/manual`

人工升级任务 Body:

```
{"task_id":1,"to_supervisor_id":"C009","reason":"need supervisor help"}
```

#### GET `/escalation/history/{task_id}`

获取任务升级审计记录

---

### 回复审批模块 reply approval

#### POST `/reply/generate-draft/{message_id}`

生成回复草稿，低风险尝试自动模板回复 Response 区分 auto_sent /pending_review

#### POST `/draft/{draft_id}/approve`

人工批准草稿 Body `{"reviewer_id":"C001"}`

#### POST `/draft/{draft_id}/reject`

驳回草稿 Body `{"reviewer_id":"C001"}`

#### GET `/draft/list/{message_id}`

获取该消息全部草稿记录

---

### 联系人人工干预（星标、手动加分）

#### POST `/contact/override`

```
{
   "contact_id":"C001",
   "is_starred":1,
   "manual_bonus":15,
   "operator_id":"C018",
   "note":"important customer manually starred"
}
```

### 错误统一返回格式

```
{"ok":false,"error":"error message text"}
```

```
