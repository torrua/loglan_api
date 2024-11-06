from __future__ import annotations

from typing import TypeVar, Callable, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from loglan_core import Base as BaseORMModel
from loglan_core.addons.base_selector import BaseSelector
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from starlette.requests import Request

from app.engine import get_db, API_PATH, API_VERSION
from app.models import Base

T = TypeVar("T", bound=BaseORMModel)


def create_router(
    orm_model: T,
    base_response_model: Base,
    detailed_response_model: Base,
    validate_func: Optional[Callable[[Base, Row[T]], None]] = None,
) -> APIRouter:
    router = APIRouter(
        prefix=f"/{API_PATH}/{API_VERSION}/{orm_model.__tablename__.lower()}",
        tags=[orm_model.__tablename__.capitalize()],
    )

    @router.get(
        "/",
        response_model=List[detailed_response_model | base_response_model],
        summary=f"Get items from {orm_model.__tablename__}",
    )
    async def get_item(
        request: Request,
        db: AsyncSession = Depends(get_db),
    ) -> List[detailed_response_model | base_response_model]:

        params = dict(request.query_params)
        orm_fields = sorted(column.name for column in inspect(orm_model).c)
        detailed = params.pop("detailed", "false") == "true"
        case_sensitive = params.pop("case_sensitive", "false") == "true"
        query = BaseSelector(model=orm_model, case_sensitive=case_sensitive)

        if detailed:
            query = query.with_relationships()

        if params:
            validate_query_params(params, orm_fields)
            query = query.where_like(**params)

        items = await query.all_async(session=db, unique=detailed)
        response_model = detailed_response_model if detailed else base_response_model

        if items is None:
            raise HTTPException(
                status_code=404, detail=f"{orm_model.__name__} not found"
            )

        response = []

        for item in items:
            data = response_model.model_validate(item)

            if validate_func and detailed:
                validate_func(data, item)

            response.append(data)

        return response

    def validate_query_params(params: dict, orm_fields: List[str]) -> None:
        """
        Validate the query parameters

        Args:
            params: The request object
            orm_fields: The list of ORM fields

        Raises:
            HTTPException: If the query parameter is not in the list of ORM fields
        """
        for param in params.keys():
            if param not in orm_fields:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid query parameter: {param}. "
                        f"Allowed parameters are: {', '.join(orm_fields)}"
                    ),
                )

    return router
