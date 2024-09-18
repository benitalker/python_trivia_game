from dataclasses import dataclass


@dataclass
class Answer:
   question_id: int
   incorrect_answer: str
   id: int = None
   