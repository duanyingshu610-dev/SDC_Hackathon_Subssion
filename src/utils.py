"""Small, deterministic helpers for the triage demonstration."""

ROLE_WEIGHT = {
    "supervisor": 25,
    "customer": 20,
    "colleague": 10,
    "supplier": 8,
}

URGENCY_KEYWORDS = (
    "urgent", "immediately", "asap", "right away", "紧急", "立即", "马上",
    "deadline", "截止", "segera", "hari ini", "within minutes",
)
IMPORTANCE_KEYWORDS = (
    "login error", "incident", "outage", "故障", "无法使用", "交付",
    "demo", "launch", "payment issue", "fraud",
)
LOW_RISK_KEYWORDS = (
    "opening hours", "service hours", "brochure", "general enquiry",
    "工作时间", "客服时间", "咨询", "when you have a chance", "no rush",
)


def calculate_message_score(
    sender_role: str,
    is_starred: int,
    manual_bonus: int,
    content: str,
) -> dict:
    """Return a transparent rule-based score; this is not an ML prediction."""
    text = str(content or "").casefold()
    importance = sum(14 for keyword in IMPORTANCE_KEYWORDS if keyword.casefold() in text)
    urgency = sum(12 for keyword in URGENCY_KEYWORDS if keyword.casefold() in text)
    base = ROLE_WEIGHT.get(str(sender_role or "").casefold(), 5)
    base += (15 if is_starred else 0) + int(manual_bonus or 0)

    total = min(base + importance + urgency, 100)
    if total >= 70:
        tier = "P1"
    elif total >= 50:
        tier = "P2"
    elif total >= 30:
        tier = "P3"
    else:
        tier = "P4"

    if any(keyword.casefold() in text for keyword in LOW_RISK_KEYWORDS):
        risk = "low"
    elif urgency + importance >= 20:
        risk = "high"
    else:
        risk = "medium"

    return {
        "importance_score": importance,
        "urgency_score": urgency,
        "computed_total_score": total,
        "assigned_tier": tier,
        "risk_level": risk,
    }
