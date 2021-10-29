# -*- coding: utf-8 -*-
"""
    src.common.scopes
    ~~~~~~~~~~~~~~~~~
    Defines authorization scopes
"""
from enum import Flag, auto
from typing import List


class Scope(Flag):
    """API Scopes with the convension Resource_Action"""
    Hacker_Read = auto()
    Hacker_Manage = auto()
    Hacker_Accept = auto()
    ClubEvent_Refresh = auto()
    Email_Send = auto()
    Event_Create = auto()
    Event_Update = auto()
    Sponsor_Create = auto()

    @property
    def names(self) -> List[str]:
        """A list of the names of all the enums this value matches"""
        return [k for k, v in self.members().items() if v & self]

    @staticmethod
    def members() -> dict:
        return {r.name: r for r in Scope}

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
