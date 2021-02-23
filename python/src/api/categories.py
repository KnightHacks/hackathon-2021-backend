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
from flask import Blueprint, request
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

    data["sponsor"] = Sponsor.objects(sponsor_name=data["sponsor"]).first()

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
          schema:
            type: string
          description: The name of the category.
        - name: sponsor
          in: query
          schema:
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
    query = {}

    if args.get("name"):
        query["name"] = args["name"]

    if args.get("sponsor"):
        sponsor_find = Sponsor.objects(sponsor_name=args["sponsor"]).first()
        if not sponsor_find:
            raise NotFound("A sponsor with that name does not exist!")
        query["sponsor"] = sponsor_find

    cat = Category.objects(**query)
    if not cat:
        raise NotFound("Sorry, no categories exist that match the query.")

    if data.get("sponsor"):
        data["sponsor"] = Sponsor.objects(sponsor_name=data["sponsor"]).first()

        if not data.get("sponsor"):
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
          schema:
            type: string
          description: The name of the category.
        - name: sponsor
          in: query
          schema:
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
            description: Sorry, no categories exist that match the query.
        5XX:
            description: Unexpected error.
    """
    args = request.args
    query = {}

    if args.get("name"):
        query["name"] = args["name"]

    if args.get("sponsor"):
        sponsor_find = Sponsor.objects(sponsor_name=args["sponsor"]).first()
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
          schema:
            type: string
          description: The name of the category.
        - name: sponsor
          in: query
          schema:
            type: string
          description: The name of the sponsor.
    responses:
        201:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            count:
                                type: integer
                                description: >
                                    The number of Categories that match the
                                    query.
                            categories:
                                type: array
                                items:
                                    $ref: '#/components/schemas/Category'
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
    query = {}

    if args.get("name"):
        query["name"] = args["name"]

    if args.get("sponsor"):
        sponsor_find = Sponsor.objects(sponsor_name=args["sponsor"]).first()
        if not sponsor_find:
            raise NotFound("A sponsor with that name does not exist!")
        query["sponsor"] = sponsor_find

    cat = Category.objects(**query).exclude("id")
    if not cat:
        raise NotFound("Sorry, no categories exist that match the query.")

    cat_list = []
    for c in cat:
        c_dict = c.to_mongo().to_dict()
        c_dict["sponsor"] = c.sponsor.sponsor_name
        cat_list.append(c_dict)

    res = {
        "count": cat.count(),
        "categories": cat_list
    }

    return res, 201
