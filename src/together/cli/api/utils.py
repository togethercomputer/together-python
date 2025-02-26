from __future__ import annotations

from gettext import gettext as _
from typing import Literal

import click


class AutoIntParamType(click.ParamType):
    name = "integer_or_max"
    _number_class = int

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> int | Literal["max"] | None:
        if value == "max":
            return "max"
        try:
            return int(value)
        except ValueError:
            self.fail(
                _("{value!r} is not a valid {number_type}.").format(
                    value=value, number_type=self.name
                ),
                param,
                ctx,
            )


class BooleanWithAutoParamType(click.ParamType):
    name = "boolean_or_auto"

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> bool | Literal["auto"] | None:
        if value == "auto":
            return "auto"
        try:
            return bool(value)
        except ValueError:
            self.fail(
                _("{value!r} is not a valid {type}.").format(
                    value=value, type=self.name
                ),
                param,
                ctx,
            )


INT_WITH_MAX = AutoIntParamType()
BOOL_WITH_AUTO = BooleanWithAutoParamType()
