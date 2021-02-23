# -*- coding: utf-8 -*-
"""
    src.api.categories
    ~~~~~~~~~~~~~~~~~~

    Functions:

        create_category
        edit_category
        get_category
        delete_category

"""
from Flask import Blueprint, request
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from src.models.category import Category
from src.models.sponsor import Sponsor


categories_blueprint = Blueprint("categories", __name__)


@categories_blueprint.route("/categories/", methods=["POST"])
def create_category():
    """
    Creates a Category
    ---
    tags:
        - category
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Category'
        description: Created Category Object
        required: true
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        404:
            description: Sorry, no sponsors exist with the provided name.
        409:
            description: Sorry, a category with that name already exists.
        5XX:
            description: Unexpected error.
    """
    data = request.get_json()

    if not data:
        raise BadRequest()

    data["sponsor"] = Sponsor.findOne(sponsor_name=data["sponsor"])

    if not data["sponsor"]:
        raise NotFound("A sponsor with that name does not exist.")

    try:
        Category.createOne(**data)
    except NotUniqueError:
        raise Conflict("Sorry, a category with that name already exists.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Category was created!"
    }

    return res, 201


@categories_blueprint.route("/categories/", methods=["PUT"])
def edit_category():
    """
    Edits a Category
    ---
    tags:
        - category
    parameters:
        - name: name
          in: query
          type: string
          description: The name of the category.
        - name: sponsor
          in: query
          type: string
          description: The name of the sponsor.
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Category'
        description: Updated Category Object
        required: true
    responses:
        201:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            affected:
                                type: integer
                                description: >
                                    Number of Categories affected.
        400:
            description: Bad request.
        404:
            description: Sorry, no categories exist that match the query.
        409:
            description: Sorry, a category with that name already exists.
        5XX:
            description: Unexpected error.
    """
    args = request.args
    data = request.get_json()
    query = dict(name=args["name"])

    if args.get("sponsor"):
        sponsor_find = Sponsor.findOne(sponsor_name=args["sponsor"])
        if not sponsor_find:
            raise NotFound("A sponsor with that name does not exist!")
        query["sponsor"] = sponsor_find

    cat = Category.objects(**query)
    if not cat:
        raise NotFound("Sorry, no categories exist that match the query.")

    if data["sponsor"]:
        data["sponsor"] = Sponsor.findOne(sponsor_name=data["sponsor"])

    if not data["sponsor"]:
        raise NotFound("A sponsor with that name does not exist!")

    try:
        affected = cat.update(**data)
    except NotUniqueError:
        raise Conflict("Sorry, a category already exists with that name.")
    except ValidationError:
        raise BadRequest()

    res = dict(affected=affected)

    return res, 201


@categories_blueprint.route("/categories/", methods=["DELETE"])
def delete_category():
    """
    Deletes a Category
    ---
    tags:
        - category
    parameters:
        - name: name
          in: query
          type: string
          description: The name of the category.
        - name: sponsor
          in: query
          type: string
          description: The name of the sponsor.
    responses:
        201:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            affected:
                                type: integer
                                description: >
                                    Number of Categories affected.
        400:
            description: Bad request.
        404:
            description: Sorry, a category with that name does not exist.
        5XX:
            description: Unexpected error.
    """
    args = request.args
    query = dict(name=args["name"])

    if args.get("sponsor"):
        sponsor_find = Sponsor.findOne(sponsor_name=args["sponsor"])
        if not sponsor_find:
            raise NotFound("A sponsor with that name does not exist!")
        query["sponsor"] = sponsor_find

    cat = Category.objects(**query)
    if not cat:
        raise NotFound("Sorry, no categories exist that match the query.")

    affected = cat.delete()

    res = dict(affected=affected)

    return res, 201


@categories_blueprint.route("/categories/", methods=["GET"])
def get_category():
    """
    Gets a Category
    ---
    tags:
        - category
    parameters:
        - name: name
          in: query
          type: string
          description: The name of the category.
        - name: sponsor
          in: query
          type: string
          description: The name of the sponsor.
    responses:
        201:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            affected:
                                type: integer
                                description: >
                                    Number of Categories affected.
        400:
            description: Bad request.
        409:
            description: Sorry, a category with that name already exists.
        5XX:
            description: Unexpected error.
    """
    pass
