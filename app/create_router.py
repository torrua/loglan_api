from __future__ import annotations

from typing import TypeVar, Callable, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from loglan_core import Base as BaseORMModel
from loglan_core.addons.base_selector import BaseSelector
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from starlette.requests import Request

from app.engine import get_db
from app.models import Base

T = TypeVar("T", bound=BaseORMModel)


def create_router(
    orm_model: T,
    base_response_model: Base,
    detailed_response_model: Base,
    validate_func: Optional[Callable[[Base, Row[T]], None]] = None,
) -> APIRouter:
    router = APIRouter(
        prefix=f"/api/v2/{orm_model.__tablename__.lower()}",
        tags=[orm_model.__tablename__.capitalize()],
    )

    @router.get("/all", response_model=List[base_response_model])
    async def get_items(
        db: AsyncSession = Depends(get_db),
    ) -> List[base_response_model]:
        result = await db.execute(BaseSelector(model=orm_model).get_statement())
        items = result.scalars().all()
        if items is None:
            raise HTTPException(
                status_code=404, detail=f"{orm_model.__name__}s not found"
            )
        response = [base_response_model.model_validate(item) for item in items]
        return response

    @router.get("/", response_model=detailed_response_model)
    async def get_item(
        request: Request,
        db: AsyncSession = Depends(get_db),
    ) -> detailed_response_model:

        orm_fields = sorted(column.name for column in inspect(orm_model).c)

        await validate_query_params(request, orm_fields)

        # Check for the required 'id' parameter
        if id_param := request.query_params.get("id", None):
            id_ = int(id_param)
        else:
            raise HTTPException(
                status_code=400, detail=f"{orm_model.__name__} ID is required"
            )

        query = (
            BaseSelector(model=orm_model)
            .with_relationships()
            .filter_by(id=id_)
            .get_statement()
        )
        result = await db.execute(query)
        item = result.scalars().first()

        if item is None:
            raise HTTPException(
                status_code=404, detail=f"{orm_model.__name__} not found"
            )

        response = detailed_response_model.model_validate(item)

        if validate_func:
            validate_func(response, item)
        return response

    async def validate_query_params(request: Request, orm_fields: List[str]) -> None:
        """
        Validate the query parameters

        Args:
            request: The request object
            orm_fields: The list of ORM fields

        Raises:
            HTTPException: If the query parameter is not in the list of ORM fields
        """
        for param in request.query_params.keys():
            if param not in orm_fields:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid query parameter: {param}. "
                        f"Allowed parameters are: {', '.join(orm_fields)}"
                    ),
                )

    return router
