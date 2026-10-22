import json
import datetime
from database import init_database, get_conn, log_event
from priority_engine import analyze_single_message, batch_analyse_all
from queue_manager import TaskQueueManager
from escalation import check_task_timeout, manual_escalate, get_escalation_history
from reply_approval import ReplyApprovalService

# ------------------------------
# 模拟少量样例消息，替代完整 messages_normalized.json
# 真实使用时替换为 open("messages_normalized.json","r").load()
# ------------------------------
SAMPLE_MESSAGES = [
    {
        "message_id": "MSG-DEMO-001",
        "platform": "whatsapp",
        "original_message_id": "wa_msg_demo01",
        "sender_id": "C001",
        "platform_sender_id": "wa_demo_client01",
        "sender_name": "Alya Tan",
        "sender_role": "customer",
        "project_id": "P001",
        "content": "The client portal shows a login error for every user. Our demo is at 3 PM today. Please help.",
        "subject": "",
        "received_at": "2026-10-20T09:00:00+08:00",
        "direction": "inbound",
        "conversation_id": "wa_chat_02",
        "attachment_count": 0,
        "ingestion_method": "synthetic_demo"
    },
    {
        "message_id": "MSG-DEMO-002",
        "platform": "whatsapp",
        "original_message_id": "wa_msg_demo02",
        "sender_id": "C043",
        "platform_sender_id": "wa_demo_demo043",
        "sender_name": "Fictional Customer 043",
        "sender_role": "customer",
        "project_id": "P010",
        "content": "Could you share the standard customer service hours for your business?",
        "subject": "",
        "received_at": "2026-10-20T09:01:00+08:00",
        "direction": "inbound",
        "conversation_id": "wa_chat_152",
        "attachment_count": 0,
        "ingestion_method": "synthetic_demo"
    }
]

SAMPLE_CONTACTS = [
    {"contact_id":"C001","platform_sender_id":"wa_demo_client01","name":"Alya Tan","sender_role":"customer","is_starred":1,"manual_importance_bonus":10,"supervisor_id":"C018"},
    {"contact_id":"C018","platform_sender_id":"wa_demo_sup018","name":"Fictional Supervisor 018","sender_role":"supervisor","is_starred":0,"manual_importance_bonus":0,"supervisor_id":None},
    {"contact_id":"C043","platform_sender_id":"wa_demo_demo043","name":"Fictional Customer 043","sender_role":"customer","is_starred":0,"manual_importance_bonus":0,"supervisor_id":"C018"}
]

SAMPLE_PROJECTS = [
    {"project_id":"P001","project_name":"Client Portal Project","assignee":"C001","supervisor_id":"C018","criticality":"high","deadline":"2026-10-25T17:00:00+08:00"},
    {"project_id":"P010","project_name":"General Service Project","assignee":"C043","supervisor_id":"C018","criticality":"medium","deadline":"2026-11-01T17:00:00+08:00"}
]

SAMPLE_TEMPLATES = [
    {"template_name":"service_hours_reply","trigger_keywords":"opening hours,service hours,工作时间,客服时间","reply_content":"Our customer service hours: Mon‑Fri 9:00‑18:00 MYT. Thank you for your enquiry.","is_active":1}
]


def seed_sample_data():
    conn = get_conn()
    cur = conn.cursor()
    # 插入联系人
    for c in SAMPLE_CONTACTS:
        cur.execute('''
        INSERT OR IGNORE INTO contacts
        (contact_id,platform_sender_id,name,sender_role,is_starred,manual_importance_bonus,supervisor_id)
        VALUES (?,?,?,?,?,?,?)
        ''',(c["contact_id"],c["platform_sender_id"],c["name"],c["sender_role"],
             c["is_starred"],c["manual_importance_bonus"],c["supervisor_id"]))
    # 插入项目
    for p in SAMPLE_PROJECTS:
        cur.execute('''
        INSERT OR IGNORE INTO projects(project_id,project_name,assignee,supervisor_id,criticality,deadline)
        VALUES (?,?,?,?,?,?)
        ''',(p["project_id"],p["project_name"],p["assignee"],p["supervisor_id"],p["criticality"],p["deadline"]))
    # 插入原始消息
    for msg in SAMPLE_MESSAGES:
        cur.execute('''
        INSERT OR IGNORE INTO raw_messages
        (message_id,platform,original_message_id,sender_id,platform_sender_id,sender_name,sender_role,
        project_id,content,subject,received_at,direction,conversation_id,attachment_count,ingestion_method)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''',(
            msg["message_id"],msg["platform"],msg["original_message_id"],msg["sender_id"],msg["platform_sender_id"],
            msg["sender_name"],msg["sender_role"],msg["project_id"],msg["content"],msg["subject"],
            msg["received_at"],msg["direction"],msg["conversation_id"],msg["attachment_count"],msg["ingestion_method"]
        ))
    # 插入回复模板
    for tpl in SAMPLE_TEMPLATES:
        cur.execute('''
        INSERT OR IGNORE INTO reply_templates(template_name,trigger_keywords,reply_content,is_active)
        VALUES (?,?,?,?)
        ''',(tpl["template_name"],tpl["trigger_keywords"],tpl["reply_content"],tpl["is_active"]))
    conn.commit()
    conn.close()
    log_event("SEED_DATA","demo","seed sample contacts,projects,messages,templates complete")
    print("[SEED] 样例数据导入完成")


def main():
    print("===== Unified Smart Message Triage & Escalation System Demo =====")
    #1.初始化数据库
    init_database()
    print("[1] 数据库初始化完成")

    #2.灌入样例数据
    seed_sample_data()

    #3.逐条分析消息，打分入任务队列
    for msg in SAMPLE_MESSAGES:
        res = analyze_single_message(msg["message_id"])
        print(f"[3] 分析消息 {msg['message_id']} | tier:{res['assigned_tier']} score:{res['computed_total_score']} risk:{res['risk_level']}")

    #4.任务队列：获取下一项（模拟点击“下一项”）
    qm = TaskQueueManager()
    next_task = qm.get_next_task(agent_id="C018")
    if next_task:
        print(f"\n[4] get_next_task(点击下一项) task_id={next_task['task_id']} tier={next_task['tier']}")
        print(f"    消息内容片段: {next_task['content'][:80]}...")

        # 模拟跳过该任务
        qm.skip_task(next_task["task_id"], note="demo skip task")
        print(f"[4‑1] skip_task 执行完毕 task_id={next_task['task_id']}")

    #5.再次取下一条任务
    next_task2 = qm.get_next_task(agent_id="C018")
    if next_task2:
        print(f"\n[5] get_next_task 第二条 task_id={next_task2['task_id']} tier={next_task2['tier']}")
        print(f"    消息片段: {next_task2['content'][:80]}...")
        task_id_2 = next_task2["task_id"]
        msg_id_2 = next_task2["message_id"]

        # 回复审批服务演示
        reply_svc = ReplyApprovalService()
        reply_result = reply_svc.try_auto_template_reply(msg_id_2, risk_level="low")
        print(f"[5‑1] 回复处理结果: {reply_result}")

        # 完成任务
        qm.complete_task(task_id_2, note="demo task completed")
        print(f"[5‑2] complete_task task_id={task_id_2}")
        reply_svc.close()

    #6.超时升级演示
    print("\n[6] 执行 check_task_timeout 扫描SLA超时任务")
    escalated_ids = check_task_timeout()
    print(f"    自动升级任务ID列表:{escalated_ids}")

    # 人工升级演示
    if next_task:
        manual_ok = manual_escalate(task_id=next_task["task_id"], to_supervisor_id="C018", reason="demo manual escalate")
        print(f"[6‑1] manual_escalate result={manual_ok}")
        hist = get_escalation_history(next_task["task_id"])
        print(f"    升级记录:{hist}")

    #7.队列统计
    summary = qm.get_pending_tasks_summary()
    print(f"\n[7] 队列待处理统计 {summary}")

    qm.close()
    print("\n==== Demo run finished, DB file: message_system.db ====")
    print("提示：真实项目替换seed_sample_data函数，读取messages_normalized.json、contacts.csv、projects.csv真实数据")


if __name__ == "__main__":
    main()
