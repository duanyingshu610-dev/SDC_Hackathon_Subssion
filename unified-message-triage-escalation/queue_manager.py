import sqlite3
from database import get_conn

class TaskQueueManager:
    def __init__(self):
        self.conn = get_conn()

    def get_next_task(self, agent_id=None):
        """获取下一个待处理任务，按优先级 P1 > P2 > P3 > P4，JOIN拿到消息content"""
        cur = self.conn.cursor()
        cur.execute('''
            SELECT tq.*, rm.content
            FROM task_queue tq
            LEFT JOIN raw_messages rm ON tq.message_id = rm.message_id
            WHERE tq.status = 'pending'
            ORDER BY CASE tq.tier
                WHEN 'P1' THEN 1
                WHEN 'P2' THEN 2
                WHEN 'P3' THEN 3
                WHEN 'P4' THEN 4
            END ASC, tq.created_at ASC
            LIMIT 1
        ''')
        task = cur.fetchone()
        return task

    def skip_task(self, task_id: int, note: str = ""):
        """跳过当前任务，状态保持pending"""
        cur = self.conn.cursor()
        cur.execute("UPDATE task_queue SET status='pending' WHERE task_id=?", (task_id,))
        self.conn.commit()
        return True

    def complete_task(self, task_id: int, note: str = ""):
        """标记任务完成，增加可选note兼容demo"""
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE task_queue
            SET status='completed', completed_at=CURRENT_TIMESTAMP
            WHERE task_id=?
        ''', (task_id,))
        self.conn.commit()
        return True

    def assign_task(self, task_id: int, agent_id: str):
        """分配任务给工作人员"""
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE task_queue
            SET assigned_agent=?
            WHERE task_id=?
        ''', (agent_id, task_id))
        self.conn.commit()
        return True

    def get_pending_tasks_summary(self):
        """统计待办任务汇总，适配demo"""
        cur = self.conn.cursor()
        cur.execute('''
            SELECT tier, COUNT(*) as cnt
            FROM task_queue
            WHERE status = 'pending'
            GROUP BY tier
        ''')
        rows = cur.fetchall()
        summary = {}
        for r in rows:
            summary[r["tier"]] = r["cnt"]
        return summary

    def close(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    print("task queue manager module loaded")
