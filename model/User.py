from dataclasses import dataclass


@dataclass
class User:
   first: str
   last: str
   email: str
   id: int = None
