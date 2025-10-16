
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class CreditLedger:
    user_id: int
    balance: int = 0
    history: List[str] = field(default_factory=list)

    def add_credit(self, amount: int):
        self.balance += amount
        self.history.append(f"+{amount} credit added (Balance: {self.balance})")

    def deduct_credit(self, amount: int):
        if self.balance < amount:
            raise ValueError("Insufficient credits")
        self.balance -= amount
        self.history.append(f"-{amount} credit deducted (Balance: {self.balance})")

    def check_balance(self):
        return self.balance


class PaymentGateway:
    def process_payment(self, user_id: int, amount: float) -> bool:
        return amount > 0


@dataclass
class User:
    name: str
    email: str
    password: str
    skills_offered: List[str]
    skills_wanted: List[str]
    credits: int = 0

    def __post_init__(self):
        self.ledger = CreditLedger(user_id=id(self), balance=self.credits)

    def view_credits(self):
        return self.ledger.check_balance()


@dataclass
class Learner(User):
    def book_session(self, teacher: 'Teacher', skill: str, time: datetime):
        return Session(teacher=teacher, learner=self, skill=skill, time=time)


@dataclass
class Teacher(User):
    rating: float = 0.0

    def earn_credits(self, amount: int):
        self.ledger.add_credit(amount)


@dataclass
class Review:
    session_id: int
    reviewer: str
    rating: int
    comment: str


@dataclass
class Session:
    teacher: Teacher
    learner: Learner
    skill: str
    time: datetime
    status: str = "scheduled"
    reviews: List[Review] = field(default_factory=list)

    def start_session(self):
        self.status = "in_progress"

    def end_session(self):
        if self.learner.ledger.balance < 1:
            raise ValueError("Insufficient credits")
        self.learner.ledger.deduct_credit(1)
        self.teacher.ledger.add_credit(1)
        self.status = "completed"

    def record_feedback(self, review: Review):
        self.reviews.append(review)
