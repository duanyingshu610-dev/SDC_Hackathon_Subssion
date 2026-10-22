# DB Schema Document
Unified Smart Message Triage & Escalation System
> SQLite database schema document, correspond to database.py

## Database File
`message_system.db`

### Table List
1. `contacts` 联系人信息（客户/供应商/同事/主管）
| Column | Type | Description |
|---|---|---|
| contact_id | TEXT PK | 联系人唯一ID C001 |
| platform_sender_id | TEXT | 各平台发送方ID |
| name | TEXT | 姓名 |
| sender_role | TEXT | customer / supplier / colleague / supervisor |
| is_starred | INTEGER | 0/1 人工星标 |
| manual_importance_bonus | INTEGER | 手动优先级加分 |
| supervisor_id | TEXT FK | 上级联系人ID |
| created_at | TIMESTAMP | 创建时间 |

2. `projects` 项目表
| Column | Type | Description |
|---|---|---|
| project_id | TEXT PK | P001‑P015 / UNASSIGNED |
| project_name | TEXT | 项目名称 |
| assignee | TEXT FK | 负责人contact_id |
| supervisor_id | TEXT FK | 项目主管ID，升级逻辑以此为准，**不依赖消息sender_role** |
| criticality | TEXT | 项目重要等级 |
| deadline | TIMESTAMP | 项目截止时间 |

3. `raw_messages` 原始消息表（保留messages_normalized.json原始字段，message_id主键，不修改）
> message_id：跨系统唯一关联主键，禁止修改原始输入message_id

4. `message_analysis` AI分析打分结果
| Column | Type | Description |
|---|---|---|
| analysis_id | INTEGER PK AUTO |
| message_id | TEXT UNIQUE FK | 关联原始消息 |
| importance_score | REAL | 重要性分数0‑100 |
| urgency_score | REAL | 紧急性分数0‑100 |
| computed_total_score | REAL | 综合总得分 |
| assigned_tier | TEXT | P1/P2/P3/P4 |
| suggested_owner | TEXT FK | 建议处理人 |
| risk_level | TEXT | low / medium / high；**只有low风险允许自动模板回复** |
| analysis_timestamp | TIMESTAMP | 分析时间 |

5. `task_queue` 核心任务队列表
| Column | Type | Description |
|---|---|---|
| task_id | INTEGER PK AUTO |
| message_id | TEXT UNIQUE FK |
| analysis_id | INTEGER FK |
| tier | TEXT | P1‑P4 |
| score | REAL | 综合分数，排序依据 |
| status | TEXT | pending / processing / completed / skipped / escalated |
| assigned_agent | TEXT FK | 当前处理人 |
| escalated_to | TEXT FK | 升级后的主管 |
| due_sla_timestamp | TIMESTAMP | SLA超时截止时间，到达该时间触发自动升级 |
| completed_at | TIMESTAMP | 任务完成时间 |
| created_at | TIMESTAMP |

6. `escalation_records` 升级审计记录，所有自动/手动升级必须写入本表留痕

7. `reply_templates` 人工预设回复模板，**AI不能自己生成模板**；只有low‑risk消息才匹配自动发送

8. `reply_drafts` 回复草稿表
> 业务规则：
> - status = sent_auto：匹配低风险模板自动发送
> - pending_review：必须人工审核，不能直接发送
> - approved：人工确认后发送
> - rejected：人工驳回

9. `contact_overrides` 人工干预审计：星标、手动重要性加分，操作员ID留痕

10. `processing_logs` 全局系统审计日志，所有关键事件写入，用于可追溯排查

11. `sla_config` SLA超时配置表
| tier | timeout_minutes | description |
|---|---|---|
| P1 | 30 | 重要且紧急 |
| P2 | 240 | 重要但不紧急 |
| P3 | 1440 | 普通 |
| P4 | 4320 | 低优先级 |

## Foreign key constraint
所有外键启用，保证数据完整性。
> 业务规则重点
> 1. 原始message_id完全保留输入值，不做改写
> 2. 升级主管来源：`projects.supervisor_id`，不能靠消息sender_role字符串判断主管
> 3. 自动回复严格限制：仅risk_level=low，匹配管理员预先录入模板，其余一律生成草稿等待人工确认，AI不可自由输出回复直接发送。
> 4. 星标、手动加分存入 contact_overrides，保留操作人，全部日志留痕审计。
