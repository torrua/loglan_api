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

router_authors = (Author, AuthorResponse, AuthorResponse, author_validator)
router_words = (Word, WordResponse, WordDetailedResponse, word_validator)
router_events = (Event, EventResponse, EventDetailedResponse, event_validator)
router_types = (Type, TypeResponse, TypeDetailedResponse, type_validator)
router_keys = (Key, KeyResponse, KeyDetailedResponse, keys_validator)
router_settings = (Setting, SettingResponse, SettingDetailedResponse, None)
router_syllables = (Syllable, SyllableResponse, SyllableDetailedResponse, None)
router_definitions = (
    Definition,
    DefinitionResponse,
    DefinitionDetailedResponse,
    definition_validator,
)

routers_data = [
    router_authors,
    router_words,
    router_definitions,
    router_events,
    router_types,
    router_keys,
    router_settings,
    router_syllables,
]

routers = [create_router(*item) for item in routers_data]
