# 消息数据字典 Data Dictionary

> 所有数据和身份均为虚构；`ingestion_method=synthetic_demo` 表示模拟接入而非真实同步。

| 字段 | 类型 | 说明 | 示例 | 主要归属 |
|---|---|---|---|---|
| message_id | string | `平台 + 原始消息ID` 的稳定哈希编号，用于去重与数据库关联 | MSG-... | 1号 |
| platform | enum | whatsapp / email / discord | email | 1号 |
| original_message_id | string | 原始平台消息标识，模拟生成 | mail_msg_001 | 1号 |
| sender_id | string | 来自联系人表的内部统一身份编号 | C001 | 1号 |
| platform_sender_id | string | 原平台发送者标识，仅为虚拟账号标识 | client01@example.com | 1号 |
| sender_name | string | 虚拟发送人显示名 | Alya Tan | 1号 |
| sender_role | enum | customer / supplier / supervisor / colleague / unknown | customer | 联系人表+1号 |
| project_id | string | 关联项目编号；模拟数据用 project_hint 提供 | P001 | 数据/业务组确认 |
| content | string | 消息正文，不含 Email 标题 | Please help... | 1号 |
| subject | string | Email 邮件标题，其他平台为空 | Project update | 1号 |
| received_at | ISO8601 | 消息收到时间，**必须有时区** | 2026-10-20T09:00:00+08:00 | 1号 |
| direction | enum | inbound/outbound，当前样例都为 inbound | inbound | 1号 |
| conversation_id | string | 模拟群/频道/邮件会话标识 | mail_thread_01 | 1号 |
| attachment_count | integer | 附件数量；此批演示数据为0 | 0 | 1号 |
| ingestion_method | string | 标记消息接入方式，用于避免误称实时同步 | synthetic_demo | 1号 |

## 参考表
`data/reference/contacts.csv`：`contact_id,platform,platform_sender_id,display_name,sender_role,organisation`。同一个联系人在3个平台可以对应同一个 `contact_id`。

`data/reference/projects.csv`：`project_id,project_name,project_deadline,assignee_id,supervisor_id,project_criticality`；时间均为合成数据。`assignee_id` 和 `supervisor_id` 是虚构成员ID，不是平台账号。

## 下一组扩展字段（本模块暂不生成）
- `importance`、`urgency`、`confidence`、`classification_reason`：2号负责分析，并提供复核机制。
- `priority_score`、`priority_tier`、`status`、`response_sla_deadline`、`escalated_at`、`reply_approval_status`：3号后端负责计算和管理。
- 不得因为原始数据带有 `project_hint`，就声称系统从聊天内容自动识别项目；那需要单独开发/验证。


## 大样本 v2 补充说明
- 每个平台3,000条有效消息；所有输出表字段与原版相同，保持兼容。
- `data/reference/synthetic_reference_labels.csv` 是独立的**合成测试参考标签**，不属于标准化消息生产字段；避免将预期答案泄漏给分类程序。
- 标签字段：`message_id`（关联键），`platform`，`scenario_tag`（模拟场景类型），`language`（en/zh/ms），`reference_importance`/`reference_urgency`（场景预设1–5），`suggested_reply_mode`（template_candidate / human_review），`annotation_source`，`difficulty`。
- 合成标签不是人工审核过的真实世界事实，预设优先级仅供开发和测试。
