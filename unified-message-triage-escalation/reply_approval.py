import sqlite3
from database import get_conn

class ReplyApprovalService:
    def __init__(self):
        self.conn = get_conn()

    def try_auto_template_reply(self, message_id: str, risk_level: str):
        cur = self.conn.cursor()
        # 拿到消息原文
        cur.execute("SELECT content FROM raw_messages WHERE message_id=?", (message_id,))
        row_msg = cur.fetchone()
        if not row_msg:
            return {"auto_sent": False, "reason": "message not found"}
        msg_content = row_msg["content"].lower()

        # 匹配模板
        cur.execute("SELECT * FROM reply_templates WHERE is_active=1")
        templates = cur.fetchall()
        matched_tpl = None
        for tpl in templates:
            keywords = tpl["trigger_keywords"].split(",")
            for kw in keywords:
                if kw.strip().lower() in msg_content:
                    matched_tpl = tpl
                    break
            if matched_tpl:
                break

        if not matched_tpl:
            return {"auto_sent": False, "reason": "no matching template"}

        # ✅ 这里字段用 draft_content，和database建表保持一致！
        cur.execute('''
            INSERT INTO reply_drafts(message_id, template_id, draft_content, status, reviewer_id)
            VALUES (?,?,?,?,?)
        ''', (message_id, matched_tpl["template_id"], matched_tpl["reply_content"], "pending", None))
        self.conn.commit()

        return {
            "auto_sent": True,
            "template_id": matched_tpl["template_id"],
            "content": matched_tpl["reply_content"]
        }

    def close(self):
        if self.conn:
            self.conn.close()
