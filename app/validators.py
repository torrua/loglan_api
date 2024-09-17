from __future__ import annotations
from loglan_core import Word, Definition, Author, Type, Event, Key

from app.models import (
    BaseWordResponse,
    BaseDefinitionResponse,
    BaseAuthorResponse,
    BaseTypeResponse,
    BaseEventResponse,
    BaseKeyResponse,
    BaseDefinitionDetailedResponse,
    BaseWordDetailedResponse,
    BaseEventDetailedResponse,
    BaseAuthorDetailedResponse,
    BaseKeyDetailedResponse,
    BaseTypeDetailedResponse,
)


async def word_validate_relationships(
    response: BaseWordDetailedResponse,
    item: Word,
) -> None:
    response.derivatives = [
        BaseWordResponse.model_validate(i) for i in item.derivatives
    ]
    response.affixes = [BaseWordResponse.model_validate(i) for i in item.affixes]
    response.affixes = [BaseWordResponse.model_validate(i) for i in item.complexes]
    response.definitions = [
        BaseDefinitionResponse.model_validate(i) for i in item.definitions
    ]
    response.authors = [BaseAuthorResponse.model_validate(i) for i in item.authors]
    response.type = BaseTypeResponse.model_validate(item.type)
    response.event_start = BaseEventResponse.model_validate(item.event_start)
    if item.event_end_id:
        response.event_end = BaseEventResponse.model_validate(item.event_end)


async def definition_validate_relationships(
    response: BaseDefinitionDetailedResponse,
    definition: Definition,
) -> None:
    response.source_word = BaseWordResponse.model_validate(definition.source_word)
    response.keys = [BaseKeyResponse.model_validate(key) for key in definition.keys]


async def event_validate_relationships(
    response: BaseEventDetailedResponse,
    item: Event,
) -> None:
    response.deprecated_words = [
        BaseWordResponse.model_validate(i) for i in item.deprecated_words
    ]
    response.appeared_words = [
        BaseWordResponse.model_validate(i) for i in item.appeared_words
    ]


async def type_validate_relationships(
    response: BaseTypeDetailedResponse,
    item: Type,
) -> None:
    response.words = [BaseWordResponse.model_validate(i) for i in item.words]


async def keys_validate_relationships(
    response: BaseKeyDetailedResponse,
    item: Key,
) -> None:
    response.definitions = [
        BaseDefinitionResponse.model_validate(i) for i in item.definitions
    ]


async def author_validate_relationships(
    response: BaseAuthorDetailedResponse,
    item: Author,
) -> None:
    response.contribution = [
        BaseWordResponse.model_validate(i) for i in item.contribution
    ]
