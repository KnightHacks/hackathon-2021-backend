# -*- coding: utf-8 -*-
"""
    src.api
    ~~~~~~~
"""
from flask import Blueprint as bp
import typing as t


class Blueprint(bp):

    def get(self, rule: str, **options: t.Any) -> t.Callable:
        return self.route(rule, **options, methods=["GET"])

    def post(self, rule: str, **options: t.Any) -> t.Callable:
        return self.route(rule, **options, methods=["POST"])

    def put(self, rule: str, **options: t.Any) -> t.Callable:
        return self.route(rule, **options, methods=["PUT"])

    def delete(self, rule: str, **options: t.Any) -> t.Callable:
        return self.route(rule, **options, methods=["DELETE"])

    def patch(self, rule: str, **options: t.Any) -> t.Callable:
        return self.route(rule, **options, methods=["PATCH"])
