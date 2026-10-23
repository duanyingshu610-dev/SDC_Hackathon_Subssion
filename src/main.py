"""Application entry point for one-message triage."""

from src.utils import ROLE_WEIGHT, calculate_message_score

SUPPORTED_PLATFORMS = {"whatsapp", "email", "discord"}


def triage_message(message: dict) -> dict:
    """Validate and score one normalized message without sending anything."""
    if not isinstance(message, dict):
        raise ValueError("input must be a JSON object")

    message_id = str(message.get("message_id", "")).strip()
    platform = str(message.get("platform", "")).strip().casefold()
    content = message.get("content")
    sender_role = str(message.get("sender_role", "customer")).strip().casefold()

    if not message_id:
        raise ValueError("message_id is required")
    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError("platform must be whatsapp, email, or discord")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("content must be a non-empty string")
    if sender_role not in ROLE_WEIGHT:
        raise ValueError("sender_role must be customer, supplier, colleague, or supervisor")

    scores = calculate_message_score(
        sender_role=sender_role,
        is_starred=int(bool(message.get("is_starred", False))),
        manual_bonus=int(message.get("manual_bonus", 0)),
        content=content,
    )
    return {
        "message_id": message_id,
        "platform": platform,
        "sender_role": sender_role,
        "content": content,
        **scores,
        "requires_human_review": True,
        "sending_enabled": False,
        "notice": "Training simulation only. This system does not send messages.",
    }
