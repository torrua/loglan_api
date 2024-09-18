from __future__ import annotations

from loglan_core import (
    Word,
    Event,
    Definition,
    Type,
    Key,
    Setting,
    Syllable,
    Author,
)

from app.models import (
    DefinitionResponse,
    WordResponse,
    KeyResponse,
    AuthorResponse,
    TypeResponse,
    EventResponse,
    SettingResponse,
    SyllableResponse,
    DefinitionDetailedResponse,
    WordDetailedResponse,
    SettingDetailedResponse,
    SyllableDetailedResponse,
    EventDetailedResponse,
    TypeDetailedResponse,
    KeyDetailedResponse,
)
from app.base import (
    create_router,
)
from app.validators import (
    word_validator,
    definition_validator,
    event_validator,
    type_validator,
    keys_validator,
    author_validator,
)

routers_data = [
    (Author, AuthorResponse, AuthorResponse, author_validator),
    (Definition, DefinitionResponse, DefinitionDetailedResponse, definition_validator),
    (Word, WordResponse, WordDetailedResponse, word_validator),
    (Event, EventResponse, EventDetailedResponse, event_validator),
    (Type, TypeResponse, TypeDetailedResponse, type_validator),
    (Key, KeyResponse, KeyDetailedResponse, keys_validator),
    (Setting, SettingResponse, SettingDetailedResponse, None),
    (Syllable, SyllableResponse, SyllableDetailedResponse, None),
]

routers = [create_router(*item) for item in routers_data]
