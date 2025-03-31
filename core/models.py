from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Person:
    name: str
    id_card: str
    gender: str
    age: int
    phone: str = ""
    address: str = ""
    position: str = ""


@dataclass
class InjuredPerson(Person):
    injury_date: Optional[datetime] = None
    injury_description: str = ""
    is_overage: bool = False


@dataclass
class Case:
    case_id: str
    case_type: str
    injured_person: InjuredPerson
    witnesses: List[Person] = None
    company: str = ""
    construction_site: str = ""
    create_time: datetime = datetime.now()
    status: str = "处理中"

    def __post_init__(self):
        if self.witnesses is None:
            self.witnesses = []