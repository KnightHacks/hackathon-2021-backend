# -*- coding: utf-8 -*-
"""
    src.common.scopes
    ~~~~~~~~~~~~~~~~~
    Defines authorization scopes
"""
from enum import Flag, auto


class Scopes(Flag):
    HackerView = auto()
    HackerAccept = auto()

    @staticmethod
    def members() -> dict:
        return {r.name: r for r in Scopes}

    @classmethod
    def _missing_(cls, value):
        members = cls.members()
        if isinstance(value, list):
            resolved = None
            for v in value:
                if resolved is None:
                    resolved = cls(v)
                else:
                    resolved = resolved | cls(v)
            if resolved is not None:
                return resolved
        if value in members.keys():
            return cls(members[value])
        return super()._missing_(value)
