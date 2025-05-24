# -*- coding: utf-8 -*-

from enum_mate import api


def test():
    _ = api
    _ = api.EnumMixin
    _ = api.BetterIntEnum
    _ = api.BetterStrEnum


if __name__ == "__main__":
    from enum_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "enum_mate.api",
        preview=False,
    )
