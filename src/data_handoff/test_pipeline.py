import json,unittest
from pathlib import Path
from message_connector import load_mock_events
from message_normalizer import load_contacts,normalize_message
B=Path(__file__).resolve().parents[1]
C=json.loads((B/'dataset_config.json').read_text())
class PipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contacts=load_contacts(B/'data/reference/contacts.csv')
        cls.events=list(load_mock_events(B/'data/raw'))
    def test_platforms_and_total(self):
        self.assertEqual(len(self.events),C['raw_events_total'])
        self.assertEqual({p for p,_ in self.events},set(C['platforms']))
    def test_replay_deduplication(self):
        msgs=[normalize_message(p,m,self.contacts) for p,m in self.events]
        self.assertEqual(len({m['message_id'] for m in msgs}),C['unique_total'])
    def test_sender_and_timezone(self):
        p,m=self.events[0]
        n=normalize_message(p,m,self.contacts)
        self.assertEqual(n['sender_role'],'customer')
        self.assertEqual(n['sender_id'],'C001')
        self.assertIn('+08:00',n['received_at'])
    def test_deterministic_message_ids(self):
        p,m=self.events[0]
        self.assertEqual(normalize_message(p,m,self.contacts)['message_id'],normalize_message(p,m,self.contacts)['message_id'])
    def test_same_platform_idempotence(self):
        p,m=self.events[0]
        self.assertEqual(normalize_message(p,m,self.contacts),normalize_message(p,m,self.contacts))
if __name__=='__main__':unittest.main()
