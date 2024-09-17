from __future__ import annotations

from typing import Callable, List

from fastapi import HTTPException, APIRouter, Depends
from loglan_core.addons.base_selector import BaseSelector
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.engine import get_db


def create_router(
    orm_model,
    base_response_model,
    detailed_response_model,
    validate_func: Callable | None = None,
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
            await validate_func(response, item)
        return response

    return router
