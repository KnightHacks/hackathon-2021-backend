# -*- coding: utf-8 -*-
"""
    src.api.live_updates
    ~~~~~~~~~~~~~~~~~~~~

    Classes:

        LiveUpdates

    Fuctions:

        new_update()
        delete_all_updates()
        delete_update(id: int)

"""
from flask import Blueprint, request
from werkzeug.exceptions import BadRequest, NotFound
from src.common.decorators import authenticate
from flask_socketio import Namespace, emit
from src.models.live_update import LiveUpdate

live_updates_blueprint = Blueprint("live_updates", __name__)


@live_updates_blueprint.route("/live_updates/", methods=["PUT"])
@authenticate
def new_update(_):
    """
    Adds an update
    ---
    tags:
        - live_updates
    requestBody:
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        message:
                            type: string
    responses:
        201:
            description: OK
        400:
            description: Bad Request.
        5XX:
            description: Unexpected error.
    """
    data = request.get_json()

    if not data or not data.get("message"):
        raise BadRequest()

    lup = LiveUpdate.createOne(message=data.get("message"))

    emit("NewLiveUpdate", {
        "data": {
            "ID": lup.ID,
            "message": data.get("message")
        }
    }, namespace="/liveupdates", broadcast=True)

    res = {
        "status": "success",
        "message": "Update sent!"
    }

    return res, 201


@live_updates_blueprint.route("/live_updates/all/", methods=["DELETE"])
@authenticate
def delete_all_updates(_):
    """
    Deletes all updates
    ---
    tags:
        - live_updates
    responses:
        201:
            description: OK
        5XX:
            description: Unexpected error.
    """

    LiveUpdate.drop_collection()

    emit("DeleteAllLiveUpdates",
         namespace="/liveupdates",
         broadcast=True)

    res = {
        "status": "success",
        "message": "Updates deleted!"
    }

    return res, 201


@live_updates_blueprint.route("/live_updates/<id>/", methods=["DELETE"])
@authenticate
def delete_update(_, id: int):
    """
    Deletes an Update
    ---
    tags:
        - live_updates
    parameters:
        -
            name: id
            in: path
            required: true
            schema:
                type: integer
    responses:
        201:
            description: OK
        404:
            description: Update not Found
        5XX:
            description: Unexpected error.
    """

    to_delete = LiveUpdate.objects(ID=id).first()

    if not to_delete:
        raise NotFound(f"LiveUpdate with the ID ${id} does not exist.")

    to_delete.delete()

    emit("DeleteLiveUpdate",
         {"data": id},
         namespace="/liveupdates",
         broadcast=True)

    res = {
        "status": "success",
        "message": "Updates deleted!"
    }

    return res, 201


"""Create the SocketIO Namespace"""


class LiveUpdates(Namespace):

    def on_connect(self):
        lups = LiveUpdate.objects.exclude("id")

        self.emit("hello", lups)

    def on_disconnect(self):
        pass

    def on_reload(self, _=None):
        lups = LiveUpdate.objects.exclude("id")

        self.emit("reload", lups)
