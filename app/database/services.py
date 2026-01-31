from app.database.db_connection import db_a_client, user_coll, todo_coll
from app.models.user import (
    delete_user_schema,
    update_user_schema,
    add_catagory_schema,
    update_catagory_schema,
    new_todo_schema,
    update_todo_schema,
    delete_todo_schema,
    update_todo_status_schema,
)
from bson import ObjectId

from app.utils.tools import (
    convert_objectid_in_doc,
    get_inserted_id,
    convert_objectid_in_list,
)
from bson import ObjectId


def is_db_a_connected():
    """check db is connected or not"""
    try:
        db_a_client.admin.command("ping")
        # print("ok")
        return True
    except:
        # print("db not connected")
        return False


def find_user(user_email: str):
    """get a user"""
    user = convert_objectid_in_doc(
        user_coll.find_one({"email": user_email}, {"passwd": 0})
    )

    if user:
        return user
    else:
        return None


def create_user(usr: dict):
    """add new user"""
    if not usr:
        return None

    res = get_inserted_id(user_coll.insert_one(usr))

    if res:
        return res
    else:
        return None


def delete_user(data: delete_user_schema):
    """delete user from app db"""
    delete_count = user_coll.delete_one(
        {"_id": ObjectId(data.user_id), "email": data.email}
    ).deleted_count
    if delete_count:
        return True
    else:
        return False


def update_user(data: update_user_schema):
    """update user data in app"""
    status = user_coll.update_one(
        {"_id": ObjectId(data.user_id)},
        ({"$set": {"name": data.name, "email": data.email, "catagory": data.catagory}}),
    ).upserted_id

    if status:
        return str(status)
    else:
        return False


def get_user(user_id: str, user_email: str):
    data = user_coll.find_one(
        {"_id": ObjectId(user_id), "email": user_email}, {"_id": 0, "passwd": 0}
    )
    if data:
        return data
    else:
        return None


def deafult_catagory(user_id: str):
    """Deafult catagory assign for todo"""
    user_coll.update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "catagory": [
                    {"catagory": "Study", "color": "245ae2"},
                    {"catagory": "Health", "color": "00e0a0"},
                    {"catagory": "Work", "color": "9c18f9"},
                ],
                "theme": False,
            }
        },
    )


def get_catagories(user_id: str):
    data = user_coll.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "catagory": 1})

    if data:
        return data
    return None


def add_catagory(data: add_catagory_schema):
    """new todo catagory"""
    status = user_coll.update_one(
        {"_id": ObjectId(data.user_id)},
        {
            "$push": {
                "catagory": {
                    "catagory": data.catagory_data.catagory,
                    "color": data.catagory_data.color,
                }
            }
        },
    ).modified_count

    print(status)

    if status:
        return True
    else:
        return False


def update_catagory(data: update_catagory_schema):
    """update whole todo catagory"""
    status = user_coll.update_one(
        {"_id": ObjectId(data.user_id)}, {"$set": {"catagory": data.catagory_data}}
    ).modified_count
    print(status)
    if status:
        return True
    else:
        return False


def delete_catagory(data: add_catagory_schema):
    """delete one todo catagory"""
    status = user_coll.update_one(
        {"_id": ObjectId(data.user_id)},
        {
            "$pull": {
                "catagory": {
                    "catagory": data.catagory_data.catagory,
                    "color": data.catagory_data.color,
                }
            }
        },
    ).modified_count

    if status:
        return True
    else:
        return False


def create_todo(data: new_todo_schema):
    """create new todo"""
    status = todo_coll.insert_one(
        {
            "title": data.title,
            "desc": data.desc,
            "due_date": data.due_date,
            "priority": data.priority,
            "catagory": data.catagory,
            "status": data.status,
            "user_id": data.user_id,
        }
    ).inserted_id

    if status:
        return str(status)
    else:
        return None


def get_one_todo(todo_id: str, user_id: str):
    """get one todo"""
    data = todo_coll.find_one(
        {"_id": ObjectId(todo_id), "user_id": user_id}, {"_id": 0}
    )
    return data


def get_all_todo(user_id: str):
    """get all todo of an user"""
    data = convert_objectid_in_list(todo_coll.find({"user_id": user_id}))
    return data


def update_todo(data: update_todo_schema):
    status = todo_coll.update_one(
        {"_id": ObjectId(data.todo_id), "user_id": data.user_id},
        {
            "$set": {
                "title": data.title,
                "desc": data.desc,
                "due_date": data.due_date,
                "priority": data.priority,
                "catagory": data.catagory,
                "status": data.status,
            }
        },
    ).modified_count
    return status


def delete_todo(data: delete_todo_schema):
    res = todo_coll.delete_one(
        {"_id": ObjectId(data.todo_id), "user_id": data.user_id}
    ).deleted_count
    return res


def update_status(data: update_todo_status_schema):
    status = todo_coll.update_one(
        {"_id": ObjectId(data.todo_id), "user_id": data.user_id},
        {"$set": {"status": data.status}},
    ).modified_count
    return status


def mark_all_done(user_id: str):
    status = todo_coll.update_many(
        {"user_id": user_id}, {"$set": {"status": 2}}
    ).modified_count
    return status


def delete_done_todo(user_id: str):
    status = todo_coll.delete_many({"user_id": user_id, "status": 2}).deleted_count
    return status
