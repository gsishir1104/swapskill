# SwapSkill

A Python domain-model prototype for booking skill-exchange sessions and transferring learning credits. It models learners, teachers, sessions, credit history, and feedback using dataclasses and the Python standard library.

This README describes the repository's default branch, `usecase-book-session`.

## Implemented workflow

1. Create learner and teacher objects with offered and wanted skills.
2. Add credits to the learner's ledger.
3. Book a session with a teacher, skill, and time.
4. Start the session.
5. End the session to deduct one learner credit, add one teacher credit, and mark the session completed.
6. Attach feedback to the session.

Ending a session with an insufficient learner balance raises `ValueError`. Credit additions and deductions are recorded in an in-memory history list.

## Design

| Component | Responsibility |
| --- | --- |
| `CreditLedger` | Balance updates and credit history |
| `User`, `Learner`, `Teacher` | Participant data, booking, and credit access |
| `Session` | Session status, credit transfer, and feedback collection |
| `Review` | Feedback data |
| `PaymentGateway` | Stub that returns whether an amount is positive |

The payment gateway does not process real payments or automatically add credits. The project has no web UI, REST API, database, or authentication implementation. Objects and credit history exist only in memory.

## Get started

Use Python 3.7 or later, which includes `dataclasses`. No third-party packages are required.

```bash
git clone --branch usecase-book-session https://github.com/gsishir1104/swapskill.git
cd swapskill
python -m unittest discover -s tests -v
```

## Example

Run from the repository root:

```python
from datetime import datetime
from swapskill.models import Learner, Teacher

learner = Learner(
    name="Learner",
    email="learner@example.com",
    password="demo-only",
    skills_offered=["Python"],
    skills_wanted=["Guitar"],
    credits=1,
)
teacher = Teacher(
    name="Teacher",
    email="teacher@example.com",
    password="demo-only",
    skills_offered=["Guitar"],
    skills_wanted=["Python"],
)

session = learner.book_session(teacher, "Guitar", datetime(2026, 10, 1, 15, 0))
session.start_session()
session.end_session()

print(session.status)         # completed
print(learner.view_credits()) # 0
print(teacher.view_credits()) # 1
```

The password field is plain object data, not secure credential storage; use dummy values when exploring the prototype.

## Tests and source

- [swapskill/models.py](swapskill/models.py): domain models and operations.
- [tests/test_booking_flow.py](tests/test_booking_flow.py): two tests covering a successful credit-transfer/feedback flow and insufficient credits.
- [swapskill/__init__.py](swapskill/__init__.py): model exports.

The prototype demonstrates object-oriented modeling, dataclasses, exception handling, and workflow tests. Session-transition validation, prevention of repeated completion, input validation, persistence, and real payment integration remain outside the current implementation.

[Author's GitHub](https://github.com/gsishir1104)
