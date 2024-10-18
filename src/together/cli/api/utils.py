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


INT_WITH_MAX = AutoIntParamType()
