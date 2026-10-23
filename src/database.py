import sqlite3
import datetime

DB_FILE = "message_system.db"

def get_conn():
    # ✅ 删掉 detect_types 参数，不再自动解析timestamp，避免T分隔的ISO时间报错
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def log_event(event_type: str, ref_id: str, message: str):
    """全局审计日志写入"""
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cur.execute('''
    INSERT INTO processing_logs(event_type, ref_id, log_msg, logged_at)
    VALUES (?,?,?,?)
    ''', (event_type, ref_id, message, now))
    conn.commit()
    conn.close()


def init_database():
    conn = get_conn()
    cur = conn.cursor()

    # 1. 联系人表 contacts
    cur.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        contact_id TEXT PRIMARY KEY,
        platform_sender_id TEXT,
        name TEXT,
        sender_role TEXT,
        is_starred INTEGER DEFAULT 0,
        manual_importance_bonus INTEGER DEFAULT 0,
        supervisor_id TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. 项目表 projects
    cur.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_id TEXT PRIMARY KEY,
        project_name TEXT,
        assignee TEXT,
        supervisor_id TEXT,
        criticality TEXT,
        deadline TEXT
    )
    ''')

    # 3. 原始消息 raw_messages
    cur.execute('''
    CREATE TABLE IF NOT EXISTS raw_messages (
        message_id TEXT PRIMARY KEY,
        platform TEXT,
        original_message_id TEXT,
        sender_id TEXT,
        platform_sender_id TEXT,
        sender_name TEXT,
        sender_role TEXT,
        project_id TEXT,
        content TEXT,
        subject TEXT,
        received_at TEXT,
        direction TEXT,
        conversation_id TEXT,
        attachment_count INTEGER,
        ingestion_method TEXT
    )
    ''')

    # 4. 消息分析打分 message_analysis
    cur.execute('''
    CREATE TABLE IF NOT EXISTS message_analysis (
        analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id TEXT UNIQUE,
        importance_score REAL,
        urgency_score REAL,
        computed_total_score REAL,
        assigned_tier TEXT,
        risk_level TEXT,
        analysis_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(message_id) REFERENCES raw_messages(message_id)
    )
    ''')

    # 5. 任务队列 task_queue
    cur.execute('''
    CREATE TABLE IF NOT EXISTS task_queue (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id TEXT UNIQUE,
        analysis_id INTEGER,
        tier TEXT,
        score REAL,
        status TEXT DEFAULT 'pending',
        assigned_agent TEXT,
        escalated_to TEXT,
        due_sla_timestamp TEXT,
        completed_at TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(message_id) REFERENCES raw_messages(message_id),
        FOREIGN KEY(analysis_id) REFERENCES message_analysis(analysis_id)
    )
    ''')

    # 6. 升级记录 escalation_records
    cur.execute('''
    CREATE TABLE IF NOT EXISTS escalation_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        from_agent TEXT,
        to_supervisor_id TEXT,
        reason TEXT,
        escalated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(task_id) REFERENCES task_queue(task_id)
    )
    ''')

    # 7. 回复模板 reply_templates
    cur.execute('''
    CREATE TABLE IF NOT EXISTS reply_templates (
        template_id INTEGER PRIMARY KEY AUTOINCREMENT,
        template_name TEXT UNIQUE,
        trigger_keywords TEXT,
        reply_content TEXT,
        is_active INTEGER DEFAULT 1
    )
    ''')

    # 8. 回复草稿 reply_drafts
    cur.execute('''
    CREATE TABLE IF NOT EXISTS reply_drafts (
        draft_id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id TEXT,
        template_id INTEGER,
        draft_content TEXT,
        status TEXT,
        reviewer_id TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        approved_at TEXT,
        FOREIGN KEY(message_id) REFERENCES raw_messages(message_id),
        FOREIGN KEY(template_id) REFERENCES reply_templates(template_id)
    )
    ''')

    # 9. 人工干预记录 contact_overrides
    cur.execute('''
    CREATE TABLE IF NOT EXISTS contact_overrides (
        override_id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_id TEXT,
        operator_id TEXT,
        override_type TEXT,
        old_value TEXT,
        new_value TEXT,
        override_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
    )
    ''')

    # 10. 审计日志 processing_logs
    cur.execute('''
    CREATE TABLE IF NOT EXISTS processing_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        ref_id TEXT,
        log_msg TEXT,
        logged_at TEXT
    )
    ''')

    # 11. SLA配置 sla_config
    cur.execute('''
    CREATE TABLE IF NOT EXISTS sla_config (
        tier TEXT PRIMARY KEY,
        timeout_minutes INTEGER,
        description TEXT
    )
    ''')

    # 初始化SLA配置，不存在才插入
    cur.execute("INSERT OR IGNORE INTO sla_config(tier, timeout_minutes, description) VALUES ('P1',30,'重要紧急')")
    cur.execute("INSERT OR IGNORE INTO sla_config(tier, timeout_minutes, description) VALUES ('P2',240,'重要不紧急')")
    cur.execute("INSERT OR IGNORE INTO sla_config(tier, timeout_minutes, description) VALUES ('P3',1440,'普通')")
    cur.execute("INSERT OR IGNORE INTO sla_config(tier, timeout_minutes, description) VALUES ('P4',4320,'低优先级')")

    conn.commit()
    conn.close()
    log_event("INIT_DB", "system", "All tables and sla config initialized")
