from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from app.database.services import (
    get_one_todo,
    get_all_todo,
    update_todo,
    delete_todo,
    update_status,
    mark_all_done,
    delete_done_todo,
    create_todo,
)
from app.models.user import (
    new_todo_schema,
    update_todo_schema,
    delete_todo_schema,
    update_todo_status_schema,
)

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.get("/one")
def one_todo(user_id: str, todo_id: str):
    try:
        data = get_one_todo(todo_id, user_id)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if data:
        return JSONResponse(content=data, status_code=status.HTTP_302_FOUND)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/status")
def update_todo_status(payload: update_todo_status_schema):
    try:
        res = update_status(payload)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    pass

    if res:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/")
def all_todo(user_id: str):
    try:
        data = get_all_todo(user_id)
    except Exception as err:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if data:
        return JSONResponse(content=data, status_code=status.HTTP_302_FOUND)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/")
def create_new_todo(payload: new_todo_schema):
    try:
        res = create_todo(payload)
    except Exception as err:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if res:
        return JSONResponse(content=res, status_code=status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)

    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/")
def update_one_todo(payload: update_todo_schema):
    try:
        res = update_todo(payload)
    except Exception as err:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if res:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/")
def delete_one_todo(payload: delete_todo_schema):
    try:
        res = delete_todo(payload)
    except Exception as err:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if res:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/all")
def mark_all_todo_done(user_id: str):
    try:
        res = mark_all_done(user_id)
    except Exception as err:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if res:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/done")
def delete_all_done_todo(user_id: str):
    try:
        res = delete_done_todo(user_id)
    except Exception as err:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if res:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
