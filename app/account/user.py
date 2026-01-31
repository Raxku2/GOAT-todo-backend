from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from app.database.services import (
    get_user,
    update_user,
    delete_user,
    get_catagories,
    add_catagory,
    update_catagory,
    delete_catagory,
)
from app.models.user import (
    add_catagory_schema,
    update_catagory_schema,
    update_user_schema,
    delete_user_schema,
)

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/")
def user(user_id: str, user_email: str):
    try:
        data = get_user(user_id=user_id, user_email=user_email)
    except Exception as e:
        print("thiis err")
        print(e)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if data:
        return JSONResponse(content=data)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/")
def user_edit(payload: update_user_schema):
    try:
        data = update_user(payload)
    except:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    if data:
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/")
def user_remove(payload: delete_user_schema):
    res = delete_user(payload)

    if res:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/catagory")
def get_user_catagory(user_id: str):
    try:
        data = get_catagories(user_id)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if data:
        return JSONResponse(content=data)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/catagory")
def create_user_catagory(payload: add_catagory_schema):

    try:
        res = add_catagory(payload)
        print(res)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if res:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.put("/catagory")
def update_user_catagory(payload: update_catagory_schema):
    try:
        res = update_catagory(payload)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if res:
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)


@router.delete("/catagory")
def delete_user_catagory(payload: add_catagory_schema):

    try:
        res = delete_catagory(payload)
    except Exception as err:
        print(err)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    if res:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
