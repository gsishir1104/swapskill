
import unittest
from datetime import datetime, timedelta
from swapskill.models import Learner, Teacher, Session, Review, PaymentGateway

class TestBookSession(unittest.TestCase):
    def setUp(self):
        self.learner = Learner(name="Akshaya", email="a@cmu.edu", password="pw",
                               skills_offered=["coding"], skills_wanted=["guitar"], credits=0)
        self.teacher = Teacher(name="Sam", email="s@cmu.edu", password="pw",
                               skills_offered=["guitar"], skills_wanted=["python"], credits=0)
        self.pg = PaymentGateway()

    def test_successful_flow(self):
        ok = self.pg.process_payment(self.learner.email, 9.99)
        self.assertTrue(ok)
        self.learner.ledger.add_credit(2)

        session = self.learner.book_session(self.teacher, "guitar", datetime.utcnow() + timedelta(days=1))
        session.start_session()
        session.end_session()

        self.assertEqual(self.learner.view_credits(), 1)
        self.assertEqual(self.teacher.view_credits(), 1)

        review = Review(session_id=id(session), reviewer=self.learner.name, rating=5, comment="Great class!")
        session.record_feedback(review)
        self.assertEqual(len(session.reviews), 1)

    def test_insufficient_credit_raises(self):
        session = self.learner.book_session(self.teacher, "guitar", datetime.utcnow())
        session.start_session()
        with self.assertRaises(ValueError):
            session.end_session()

if __name__ == "__main__":
    unittest.main()
