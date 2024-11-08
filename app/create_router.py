from typing import TypeVar, Callable, Optional

from fastapi import APIRouter, Depends, HTTPException
from loglan_core import Base as BaseORMModel
from loglan_core.addons.base_selector import BaseSelector
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from starlette.requests import Request

from app.engine import get_db, API_PATH, API_VERSION
from app.models import Base, ResponseModel

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
        response_model=ResponseModel,
        summary=f"Get items from {orm_model.__tablename__}",
    )
    async def get_item(
        request: Request,
        db: AsyncSession = Depends(get_db),
    ) -> ResponseModel:

        params = dict(request.query_params)
        detailed = params.pop("detailed", "false").lower() == "true"
        case_sensitive = params.pop("case_sensitive", "false").lower() == "true"
        orm_fields, skipped_fields = separate_params(params)

        query = BaseSelector(model=orm_model, case_sensitive=case_sensitive)

        if detailed:
            query = query.with_relationships()

        if orm_fields:
            query = query.where_like(**orm_fields)

        items = await query.all_async(session=db, unique=detailed)

        if items is None:
            raise HTTPException(
                status_code=404, detail=f"{orm_model.__name__} not found"
            )

        data = get_validated_data(items, detailed)

        result = ResponseModel(
            result=True,
            count=len(data),
            detailed=detailed,
            data=data,
            skipped_arguments=skipped_fields,
            case_sensitive=case_sensitive,
        )
        return result

    def get_validated_data(items: list, detailed: bool) -> list:
        """Get validated data from items

        Args:
            items (list): List of items to validate
            detailed (bool): Whether to validate detailed data

        Returns:
            list: Validated data
        """
        response_model = detailed_response_model if detailed else base_response_model

        response = []
        for item in items:
            data = response_model.model_validate(item)

            if validate_func and detailed:
                validate_func(data, item)

            response.append(data)
        return response

    def separate_params(params: dict) -> tuple[dict, list]:
        """
        Separate params into ORM params and skipped params

        Args:
            params (dict): Query parameters

        Returns:
            tuple[dict, list]: ORM params and skipped params
        """
        orm_fields = sorted(column.name for column in inspect(orm_model).c)
        orm_params = {k: v for k, v in params.items() if k in orm_fields}
        skipped_params = [k for k in params if k not in orm_fields]
        return orm_params, skipped_params

    return router
