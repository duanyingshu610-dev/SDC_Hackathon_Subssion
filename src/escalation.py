import sqlite3
from database import get_conn, log_event

class EscalationService:
    def __init__(self):
        self.conn = get_conn()

    def escalate_task(self, task_id: int, from_agent: str, to_supervisor_id: str, reason: str):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE task_queue
            SET escalated_to=?
            WHERE task_id=?
        ''', (to_supervisor_id, task_id))

        cur.execute('''
            INSERT INTO escalation_records(task_id, from_agent, to_supervisor_id, reason)
            VALUES (?,?,?,?)
        ''', (task_id, from_agent, to_supervisor_id, reason))
        self.conn.commit()
        self.conn.close()

        log_event("ESCALATE_TASK", str(task_id),
                  f"escalate from {from_agent} to {to_supervisor_id}, reason: {reason}")
        return True

    def get_escalation_history(self, task_id: int):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM escalation_records WHERE task_id=?
            ORDER BY escalated_at ASC
        ''', (task_id,))
        res = cur.fetchall()
        conn.close()
        return res


def manual_escalate(task_id: int, to_supervisor_id: str, reason: str, from_agent: str = "AGENT-001"):
    svc = EscalationService()
    return svc.escalate_task(task_id, from_agent, to_supervisor_id, reason)

def get_escalation_history(task_id: int):
    svc = EscalationService()
    return svc.get_escalation_history(task_id)

def check_task_timeout():
    """检查SLA超时（demo预留空实现，可后续扩展）"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM task_queue
        WHERE status='pending' AND due_sla_timestamp < CURRENT_TIMESTAMP
    ''')
    timeout_tasks = cur.fetchall()
    conn.close()
    return timeout_tasks


if __name__ == "__main__":
    print("escalation module loaded")
