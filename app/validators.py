from __future__ import annotations

from loglan_core import Word, Definition, Author, Type, Event, Key

from app.models import (
    WordResponse,
    DefinitionResponse,
    AuthorResponse,
    TypeResponse,
    EventResponse,
    KeyResponse,
    DefinitionDetailedResponse,
    WordDetailedResponse,
    EventDetailedResponse,
    AuthorDetailedResponse,
    KeyDetailedResponse,
    TypeDetailedResponse,
)


def word_validator(
    response: WordDetailedResponse,
    item: Word,
) -> None:
    response.derivatives = [WordResponse.model_validate(i) for i in item.derivatives]
    response.affixes = [WordResponse.model_validate(i) for i in item.affixes]
    response.complexes = [WordResponse.model_validate(i) for i in item.complexes]
    response.definitions = [
        DefinitionResponse.model_validate(i) for i in item.definitions
    ]
    response.authors = [AuthorResponse.model_validate(i) for i in item.authors]
    response.type = TypeResponse.model_validate(item.type)
    response.event_start = EventResponse.model_validate(item.event_start)
    if item.event_end_id:
        response.event_end = EventResponse.model_validate(item.event_end)


def definition_validator(
    response: DefinitionDetailedResponse,
    definition: Definition,
) -> None:
    response.source_word = WordResponse.model_validate(definition.source_word)
    response.keys = [KeyResponse.model_validate(key) for key in definition.keys]


def event_validator(
    response: EventDetailedResponse,
    item: Event,
) -> None:
    response.deprecated_words = [
        WordResponse.model_validate(i) for i in item.deprecated_words
    ]
    response.appeared_words = [
        WordResponse.model_validate(i) for i in item.appeared_words
    ]


def type_validator(
    response: TypeDetailedResponse,
    item: Type,
) -> None:
    response.words = [WordResponse.model_validate(i) for i in item.words]


def keys_validator(
    response: KeyDetailedResponse,
    item: Key,
) -> None:
    response.definitions = [
        DefinitionResponse.model_validate(i) for i in item.definitions
    ]


def author_validator(
    response: AuthorDetailedResponse,
    item: Author,
) -> None:
    response.contribution = [WordResponse.model_validate(i) for i in item.contribution]
