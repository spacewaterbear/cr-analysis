from dataclasses import dataclass
from enum import Enum

from pydantic.main import BaseModel

# absence_base_regex = r" ?: ?(.*?\n*)\. \n *\n+"
# absence_base_regex = r" ?: ?(.*?\n*)\.[\n ]{3,}"
absence_base_regex = r" ?: ?([A-Za-z0-9_À-ÿ , \n\.'-]+\.)"


# @dataclass
class PresenceRegexPattern(BaseModel):
    absent = "Absente?s?" + absence_base_regex
    forgive = "Excusée?s?" + absence_base_regex
    legit_forgive = "Excusée?s? au sens du règlement" + absence_base_regex
    present = "Présents" + absence_base_regex


class MemberInfo(BaseModel):
    title: str
    first_name: str
    last_name: str


class MemberPresences(BaseModel):
    presents: list[MemberInfo]
    absents: list[MemberInfo]
    forgived: list[MemberInfo]
    legit_forgived: list[MemberInfo]
