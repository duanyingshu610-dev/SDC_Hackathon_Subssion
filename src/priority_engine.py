import sqlite3
import datetime
from database import get_conn, log_event

# 优先级打分权重配置
ROLE_WEIGHT = {
    "supervisor": 25,
    "customer": 20,
    "colleague": 10,
    "supplier": 8
}


def calculate_message_score(sender_role: str, is_starred: int, manual_bonus: int, content: str):
    base_score = ROLE_WEIGHT.get(sender_role, 5)
    base_score += is_starred * 15
    base_score += manual_bonus

    urgency_keywords = ["urgent", "URGENT", "立即", "紧急", "马上", "within", "minit", "segera", "deadline", "截止"]
    importance_keywords = ["login error", "incident", "INC-", "故障", "无法使用", "交付", "demo", "launch"]

    urgency = 0
    importance = 0
    lower_content = content.lower()

    for kw in urgency_keywords:
        if kw.lower() in lower_content:
            urgency += 12
    for kw in importance_keywords:
        if kw.lower() in lower_content:
            importance += 14

    # 低风险关键词判定
    low_risk_keywords = ["opening hours", "service hour", "brochure", "price list", "general enquiry", "咨询"]
    risk_level = "medium"
    is_low_risk = any(kw.lower() in lower_content for kw in low_risk_keywords)
    if is_low_risk:
        risk_level = "low"
    else:
        if (urgency + importance) >= 20:
            risk_level = "high"

    total = base_score + urgency + importance
    total = min(total, 100)

    # Tier划分
    if total >= 70:
        tier = "P1"
    elif total >= 50:
        tier = "P2"
    elif total >= 30:
        tier = "P3"
    else:
        tier = "P4"

    return {
        "importance_score": importance,
        "urgency_score": urgency,
        "computed_total_score": round(total, 2),
        "assigned_tier": tier,
        "risk_level": risk_level
    }


def analyze_single_message(message_id: str):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT rm.*, c.is_starred, c.manual_importance_bonus
        FROM raw_messages rm
        LEFT JOIN contacts c ON rm.sender_id = c.contact_id
        WHERE rm.message_id = ?
        ''', (message_id,))
        row = cur.fetchone()
        if not row:
            return None

        sender_role = row["sender_role"]
        content = row["content"]
        is_starred = row["is_starred"] or 0
        manual_bonus = row["manual_importance_bonus"] or 0

        res = calculate_message_score(sender_role, is_starred, manual_bonus, content)

        cur.execute('''
        INSERT OR REPLACE INTO message_analysis
        (message_id, importance_score, urgency_score, computed_total_score, assigned_tier, risk_level)
        VALUES (?,?,?,?,?,?)
        ''', (message_id, res["importance_score"], res["urgency_score"],
              res["computed_total_score"], res["assigned_tier"], res["risk_level"]))
        analysis_id = cur.lastrowid

        # 查询SLA超时时间
        cur.execute("SELECT timeout_minutes FROM sla_config WHERE tier=?", (res["assigned_tier"],))
        sla_row = cur.fetchone()
        sla_min = sla_row["timeout_minutes"]
        received_str = row["received_at"]

        # ISO时间解析，标准库，无dateutil
        try:
            recv_dt = datetime.datetime.fromisoformat(received_str.replace("Z", "+00:00"))
        except ValueError:
            recv_dt = datetime.datetime.now()
        due_dt = recv_dt + datetime.timedelta(minutes=sla_min)

        # 写入任务队列
        cur.execute('''
        INSERT OR REPLACE INTO task_queue
        (message_id, analysis_id, tier, score, status, due_sla_timestamp)
        VALUES (?,?,?,?,?,?)
        ''', (message_id, analysis_id, res["assigned_tier"], res["computed_total_score"],
              "pending", due_dt.isoformat()))

        conn.commit()
    finally:
        # 【核心修复】无论正常还是异常，一定关闭连接，释放锁！
        conn.close()

    # ✅ 连接已经关闭，此时再调用log_event，不会锁库
    log_event("ANALYZE_MESSAGE", message_id,
              f"tier={res['assigned_tier']},score={res['computed_total_score']},risk={res['risk_level']}")

    return {"analysis_id": analysis_id, **res}


def batch_analyse_all():
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT message_id FROM raw_messages")
        all_msg = [r["message_id"] for r in cur.fetchall()]
    finally:
        conn.close()

    count = 0
    for mid in all_msg:
        analyze_single_message(mid)
        count += 1
    return count


if __name__ == "__main__":
    print("priority engine module loaded")
