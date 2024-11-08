from __future__ import annotations

from datetime import date, datetime
from typing import Optional, Dict, List

from pydantic import BaseModel, constr


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class WordResponse(Base):
    name: str
    type_id: int
    event_start_id: int
    event_end_id: Optional[int]
    origin: Optional[constr(max_length=128)]
    origin_x: Optional[constr(max_length=64)]
    match: Optional[constr(max_length=8)]
    rank: Optional[constr(max_length=8)]
    year: Optional[date]
    notes: Optional[Dict[str, str]]

    class Config:
        json_encoders = {date: lambda v: int(v.strftime("%Y")) if v else None}


class DefinitionResponse(Base):
    word_id: int
    position: int
    body: str
    usage: Optional[constr(max_length=64)]
    grammar_code: Optional[constr(max_length=8)]
    slots: Optional[int]
    case_tags: Optional[constr(max_length=16)]
    language: Optional[constr(max_length=16)]
    notes: Optional[constr(max_length=255)]


class AuthorResponse(Base):
    abbreviation: constr(max_length=64)
    full_name: Optional[constr(max_length=64)]
    notes: Optional[constr(max_length=128)]


class TypeResponse(Base):
    type_: constr(max_length=16)
    type_x: constr(max_length=16)
    group: constr(max_length=16)
    parentable: bool
    description: Optional[constr(max_length=255)]


class EventResponse(Base):
    event_id: int
    name: constr(max_length=64)
    date: date
    definition: str
    annotation: constr(max_length=16)
    suffix: constr(max_length=16)


class KeyResponse(Base):
    word: constr(max_length=64)
    language: constr(max_length=16)


class SettingResponse(Base):
    date: datetime
    db_version: int
    last_word_id: int
    db_release: constr(max_length=16)


class SyllableResponse(Base):
    name: constr(max_length=8)
    type_: constr(max_length=32)
    allowed: bool


class AuthorDetailedResponse(AuthorResponse):
    contribution: Optional[List[WordResponse]]


class DefinitionDetailedResponse(DefinitionResponse):
    source_word: WordResponse
    keys: Optional[List[KeyResponse]]


class EventDetailedResponse(EventResponse):
    deprecated_words: Optional[List[WordResponse]]
    appeared_words: Optional[List[WordResponse]]


class KeyDetailedResponse(KeyResponse):
    definitions: Optional[List[DefinitionResponse]]


class TypeDetailedResponse(TypeResponse):
    words: Optional[List[WordResponse]]


class WordDetailedResponse(WordResponse):
    authors: List[AuthorResponse]
    type: TypeResponse
    event_start: EventResponse
    event_end: Optional[EventResponse] = None
    definitions: List[DefinitionResponse]
    derivatives: Optional[List[WordResponse]]
    affixes: Optional[List[WordResponse]]
    complexes: Optional[List[WordResponse]]
    parents: Optional[List[WordResponse]]


class SettingDetailedResponse(SettingResponse):
    pass


class SyllableDetailedResponse(SyllableResponse):
    pass


class ResponseModel(BaseModel):
    result: bool
    skipped_arguments: Optional[List[str]]
    case_sensitive: bool
    detailed: bool
    count: int
    data: list
