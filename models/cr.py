from pydantic.main import BaseModel

# absence_base_regex = r" ?: ?(.*?\n*)\. \n *\n+"
# absence_base_regex = r" ?: ?(.*?\n*)\.[\n ]{3,}"

week_days = r"(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)"
months = r"(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)"
part_days = r"(?:matin|après-midi|soir|nuit)"
days = r"\d{1,2}.{,3}"
year = r"(?:\d{4})?"
get_presence_per_period = f"{week_days} {days} {months} {year} ?- {part_days}"

absence_base_regex_present = r" ?: ?([A-Za-z0-9_À-ÿ , \n\.'-]+\.)"
# absence_base_regex_date = r"\n+ ?([A-Za-z0-9_À-ÿ , \n\.'-]+\.)"
absence_base_regex_date = r"?([A-Za-z0-9_À-ÿ , \n\.'-]+\.)"


class PresenceRegexPattern(BaseModel):
    absent: str
    forgive: str
    legit_forgive: str
    present: str


present_template = "Présents :"
date_template = "Listes des membres présents."
presence_regex_mapping = {
    present_template : PresenceRegexPattern(absent="Absente?s?" + absence_base_regex_present,
                                       forgive="Excusée?s?" + absence_base_regex_present,
                                       legit_forgive="Excusée?s? au sens du règlement" + absence_base_regex_present,
                                       present="Présents" + absence_base_regex_present),

    date_template: PresenceRegexPattern(absent="Absente?s?" + absence_base_regex_present,
                                                         forgive="Excusée?s?" + absence_base_regex_present,
                                                         legit_forgive="Excusée?s? au sens du règlement" + absence_base_regex_present,
                                                         present=get_presence_per_period + absence_base_regex_date),

}


class MemberInfo(BaseModel):
    title: str
    first_name: str
    last_name: str


class MemberPresences(BaseModel):
    presents: list[MemberInfo]
    absents: list[MemberInfo]
    forgived: list[MemberInfo]
    legit_forgived: list[MemberInfo]
