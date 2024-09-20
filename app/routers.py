from __future__ import annotations

from loglan_core import (
    Author,
    Definition,
    Event,
    Key,
    Setting,
    Syllable,
    Type,
    Word,
)

from app.create_router import create_router
from app.models import (
    AuthorResponse,
    DefinitionResponse,
    EventResponse,
    KeyResponse,
    SettingResponse,
    SyllableResponse,
    TypeResponse,
    WordResponse,
    AuthorDetailedResponse,
    DefinitionDetailedResponse,
    EventDetailedResponse,
    KeyDetailedResponse,
    SettingDetailedResponse,
    SyllableDetailedResponse,
    TypeDetailedResponse,
    WordDetailedResponse,
)
from app.validators import (
    author_validator,
    definition_validator,
    event_validator,
    keys_validator,
    type_validator,
    word_validator,
)

routers_data = [
    (Author, AuthorResponse, AuthorDetailedResponse, author_validator),
    (Definition, DefinitionResponse, DefinitionDetailedResponse, definition_validator),
    (Event, EventResponse, EventDetailedResponse, event_validator),
    (Key, KeyResponse, KeyDetailedResponse, keys_validator),
    (Setting, SettingResponse, SettingDetailedResponse, None),
    (Syllable, SyllableResponse, SyllableDetailedResponse, None),
    (Type, TypeResponse, TypeDetailedResponse, type_validator),
    (Word, WordResponse, WordDetailedResponse, word_validator),
]

routers = [
    create_router(model, response_model, detailed_response_model, validator)
    for model, response_model, detailed_response_model, validator in routers_data
]
