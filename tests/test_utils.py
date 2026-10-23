import unittest

from src.main import triage_message
from src.utils import calculate_message_score


class TriageTests(unittest.TestCase):
    def test_routine_message_is_not_urgent(self):
        result = calculate_message_score("customer", 0, 0, "No rush, please send the brochure when you have a chance.")
        self.assertEqual(result["urgency_score"], 0)
        self.assertEqual(result["risk_level"], "low")

    def test_urgent_incident_scores_higher(self):
        result = calculate_message_score("customer", 0, 0, "Urgent: login error before today's demo.")
        self.assertGreater(result["computed_total_score"], 20)
        self.assertIn(result["assigned_tier"], {"P1", "P2", "P3"})

    def test_triage_output_never_sends_messages(self):
        result = triage_message({
            "message_id": "MSG-TEST-1",
            "platform": "email",
            "sender_role": "customer",
            "content": "Could you share the service hours?",
        })
        self.assertFalse(result["sending_enabled"])
        self.assertTrue(result["requires_human_review"])

    def test_invalid_platform_is_rejected(self):
        with self.assertRaises(ValueError):
            triage_message({"message_id": "MSG-1", "platform": "sms", "content": "Hello"})


if __name__ == "__main__":
    unittest.main()
