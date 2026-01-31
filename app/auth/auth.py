from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from app.auth.services import verify_auth_token
from app.database.services import find_user, create_user
from app.utils.tools import convert_objectid_in_doc
from app.database.services import deafult_catagory

router = APIRouter(prefix="/auth", tags=["Authenticate"])


@router.get("/")
def auth(authToken: str):
    """
    :param authToken: Auth token from GOAT auth
    :type authToken: str
    """
    if not authToken:
        return JSONResponse({}, status_code=status.HTTP_400_BAD_REQUEST)

    try:
        verify_status = verify_auth_token(authToken=authToken)
        if verify_status:
            verify_data = verify_status.json()
            print("verify data", verify_data)
        else:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(Exception)
        print("eta error")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    user_email = verify_data.get("usr").get("email")
    user_in_app_db = find_user(user_email)

    if user_in_app_db:
        return JSONResponse(content=user_in_app_db, status_code=status.HTTP_302_FOUND)

    else:
        result = create_user(verify_data.get("usr"))

        if result:
            print("verify data 2", verify_data)
            verify_data["_id"] = result
            verify_data = convert_objectid_in_doc(verify_data)

            deafult_catagory(result)

            return JSONResponse(
                content=verify_data["usr"], status_code=status.HTTP_201_CREATED
            )
            # return "ok"
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
