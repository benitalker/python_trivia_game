from dataclasses import dataclass


@dataclass
class Question:
   question_text: str
   correct_answer: str
   id: int = None
