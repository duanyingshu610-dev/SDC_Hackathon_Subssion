# 1号成员 | 9,000条消息大样本模拟接入指南

## 你需要做的步骤
1. 下载并解压整个 ZIP，PyCharm 的 `File → Open` 打开 `SDC_Domain2_Member1_Integration_Kit_Large` 文件夹。
2. 在项目最外层运行 `run_demo.py`（或者 Terminal 输入 `python run_demo.py`）。无需安装额外软件包。
3. 确认屏幕出现：9,270 raw events；9,000 normalized messages；270 duplicates removed；0 failed events。
4. 再运行 `validate_output.py`，确认输出 `PASS`。
5. 运行 `python -m unittest discover -s tests -v` 验证代码逻辑。
6. 打开 `output/`：`messages_normalized.csv` 给数据/AI组，`messages_normalized.json` 给后端组；`ingestion_report.json` 给测试组。
7. 一并分享 `data_dictionary.md`、`data/reference/contacts.csv`、`data/reference/projects.csv`。

## 数据规模
- WhatsApp: 3,000条唯一虚拟消息 + 90次重复投递
- Email: 3,000条唯一虚拟消息 + 90次重复投递
- Discord: 3,000条唯一虚拟消息 + 90次重复投递
- 合计: 9,000条不同 `message_id`，原始事件9,270条
- 模拟联系人60名 × 3个平台映射；虚构项目15个
- 英文、中文、马来文文本，含“紧急/不紧急”的边界场景

## 给2号 AI组
- `output/messages_normalized.csv`
- `data/reference/synthetic_reference_labels.csv`（**只作参考预期标签，不是真实人工评估**）
- `data/reference/contacts.csv`、`projects.csv`、`data_dictionary.md`
- 重要：`synthetic_reference_labels.csv` 里的 `reference_importance`、`reference_urgency` 是预先编排的测试场景目标，模型训练/评估要避免同模板内容同时出现在训练集和测试集，否则测试分数会虚高。日后必须补充人工复核样本。
- `suggested_reply_mode=template_candidate` 只是“可能适合模板”的标记，不代表系统已获授权发出消息。

## 给3号 后端组
- `output/messages_normalized.json`
- 两个引用表和字段说明
- `message_id` 作为消息去重键；真实系统还应做跨平台联系人权限控制与失败重试。
- 样本不含已计算的优先级排序和已触发升级的记录，这部分应由3号实现。

## 合规性和限制
- 所有消息、账号、联系人、项目、订单编号均虚构；不含真实私人聊天。
- 本数据 `schema` 标为 `SIMULATED_PLATFORM_EVENT_NOT_OFFICIAL_API`，**不可声称已经实现真实消息同步或实时自动回复**。
- 此脚本不需要 API 密钥或联网，不会实际向任何平台发送消息。
- 输出是静态合成数据，重新运行不会无限累积；若需换一批不同样本，需要修改生成脚本的种子并重新生成。
- 仍需按比赛规定记录 AI 使用、数据来源与 Replit 使用情况。
