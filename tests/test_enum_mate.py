# -*- coding: utf-8 -*-

import pytest
from enum_mate.impl import (
    BetterIntEnum,
    BetterStrEnum,
)


# ------------------------------------------------------------------------------
# Define enums for testing
# ------------------------------------------------------------------------------
class CodeEnum(BetterIntEnum):
    succeeded = 1
    failed = 0


class StatusEnum(BetterStrEnum):
    succeeded = "SUCCEEDED"
    failed = "FAILED"


class EmptyIntEnum(BetterIntEnum):
    pass


class EmptyStrEnum(BetterStrEnum):
    pass


class SingleIntEnum(BetterIntEnum):
    only_value = 42


class SingleStrEnum(BetterStrEnum):
    only_value = "SINGLE"


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------
class TestMixin:
    """Test the base Mixin functionality."""

    def test_get_by_name_success(self):
        assert CodeEnum.get_by_name("succeeded") is CodeEnum.succeeded
        assert CodeEnum.get_by_name("failed") is CodeEnum.failed

    def test_get_by_name_keyerror(self):
        with pytest.raises(KeyError):
            CodeEnum.get_by_name("nonexistent")
        with pytest.raises(KeyError):
            CodeEnum.get_by_name("SUCCEEDED")  # Case sensitive
        with pytest.raises(KeyError):
            CodeEnum.get_by_name("")
        with pytest.raises(KeyError):
            CodeEnum.get_by_name(" succeeded")  # Leading space
        with pytest.raises(KeyError):
            CodeEnum.get_by_name("succeeded ")  # Trailing space

    def test_get_by_name_wrong_types(self):
        with pytest.raises(KeyError):
            CodeEnum.get_by_name(1)
        with pytest.raises(KeyError):
            CodeEnum.get_by_name(None)
        with pytest.raises(TypeError):
            CodeEnum.get_by_name([])  # unhashable type: list
        with pytest.raises(TypeError):  # unhashable type: dict
            CodeEnum.get_by_name({})

    def test_is_valid_name_success(self):
        assert CodeEnum.is_valid_name("succeeded") is True
        assert CodeEnum.is_valid_name("failed") is True

    def test_is_valid_name_failure(self):
        assert CodeEnum.is_valid_name("nonexistent") is False
        assert CodeEnum.is_valid_name("SUCCEEDED") is False
        assert CodeEnum.is_valid_name("") is False
        assert CodeEnum.is_valid_name(" succeeded") is False
        assert CodeEnum.is_valid_name("succeeded ") is False
        assert CodeEnum.is_valid_name(1) is False
        assert CodeEnum.is_valid_name(None) is False
        with pytest.raises(TypeError):  # unhashable type: list
            assert CodeEnum.is_valid_name([]) is False
        with pytest.raises(TypeError):  # unhashable type: list
            assert CodeEnum.is_valid_name({}) is False  # unhashable type: dict

    def test_get_names_multiple_values(self):
        names = CodeEnum.get_names()
        assert names == ["succeeded", "failed"]
        assert isinstance(names, list)
        assert all(isinstance(name, str) for name in names)

    def test_get_names_single_value(self):
        names = SingleIntEnum.get_names()
        assert names == ["only_value"]

    def test_get_names_empty(self):
        names = EmptyIntEnum.get_names()
        assert names == []


class TestBetterIntEnum:
    """Comprehensive tests for BetterIntEnum."""

    def test_enum_basic_functionality(self):
        """Test that it still works as a regular enum."""
        assert CodeEnum.succeeded == 1
        assert CodeEnum.failed == 0

        # Test arithmetic operations
        assert CodeEnum.succeeded + 1 == 2
        assert CodeEnum.succeeded - CodeEnum.failed == 1

        # Test comparisons
        assert CodeEnum.succeeded > CodeEnum.failed
        assert CodeEnum.succeeded != CodeEnum.failed

        # Test collections
        assert {CodeEnum.succeeded, CodeEnum.failed} == {0, 1}
        assert CodeEnum.succeeded in [0, 1, 2]

    def test_get_by_value_success(self):
        assert CodeEnum.get_by_value(1) is CodeEnum.succeeded
        assert CodeEnum.get_by_value(0) is CodeEnum.failed

    def test_get_by_value_valueerror(self):
        with pytest.raises(ValueError):
            CodeEnum.get_by_value(999)
        with pytest.raises(ValueError):
            CodeEnum.get_by_value(-999)
        with pytest.raises(ValueError):
            CodeEnum.get_by_value(3)

    def test_get_by_value_wrong_types(self):
        with pytest.raises((ValueError, TypeError)):
            CodeEnum.get_by_value("1")
        with pytest.raises((ValueError, TypeError)):
            CodeEnum.get_by_value(None)
        with pytest.raises((ValueError, TypeError)):
            CodeEnum.get_by_value([])
        with pytest.raises((ValueError, TypeError)):
            CodeEnum.get_by_value(1.5)

    def test_is_valid_value_success(self):
        assert CodeEnum.is_valid_value(1) is True
        assert CodeEnum.is_valid_value(0) is True

    def test_is_valid_value_failure(self):
        assert CodeEnum.is_valid_value(999) is False
        assert CodeEnum.is_valid_value(-999) is False
        assert CodeEnum.is_valid_value(3) is False
        assert CodeEnum.is_valid_value("1") is False
        assert CodeEnum.is_valid_value(None) is False
        assert CodeEnum.is_valid_value([]) is False
        assert CodeEnum.is_valid_value(1.5) is False

    def test_ensure_is_valid_value_success(self):
        # Should not raise any exceptions
        CodeEnum.ensure_is_valid_value(1)
        CodeEnum.ensure_is_valid_value(0)

    def test_ensure_is_valid_value_failure(self):
        with pytest.raises(
            ValueError, match="Invalid `class test_enum_mate.CodeEnum`: 999"
        ):
            CodeEnum.ensure_is_valid_value(999)
        with pytest.raises(
            ValueError, match="Invalid `class test_enum_mate.CodeEnum`: -999"
        ):
            CodeEnum.ensure_is_valid_value(-999)
        with pytest.raises(
            ValueError, match="Invalid `class test_enum_mate.CodeEnum`: 3"
        ):
            CodeEnum.ensure_is_valid_value(3)

    def test_ensure_int_with_int_values(self):
        assert CodeEnum.ensure_int(1) == 1
        assert CodeEnum.ensure_int(0) == 0

        # Verify return type
        result = CodeEnum.ensure_int(1)
        assert isinstance(result, int)
        assert type(result) is int

    def test_ensure_int_with_enum_values(self):
        assert CodeEnum.ensure_int(CodeEnum.succeeded) == 1
        assert CodeEnum.ensure_int(CodeEnum.failed) == 0

        # Verify return type
        result = CodeEnum.ensure_int(CodeEnum.succeeded)
        assert isinstance(result, int)
        assert type(result) is int

    def test_ensure_int_invalid_values(self):
        with pytest.raises(ValueError):
            CodeEnum.ensure_int(999)
        with pytest.raises(ValueError):
            CodeEnum.ensure_int(-999)
        with pytest.raises((ValueError, TypeError)):
            CodeEnum.ensure_int("1")
        with pytest.raises((ValueError, TypeError)):
            CodeEnum.ensure_int(None)

    def test_get_values_multiple(self):
        values = CodeEnum.get_values()
        assert values == [1, 0]
        assert isinstance(values, list)
        assert all(isinstance(val, int) for val in values)

    def test_get_values_single(self):
        values = SingleIntEnum.get_values()
        assert values == [42]

    def test_get_values_empty(self):
        values = EmptyIntEnum.get_values()
        assert values == []

    def test_edge_cases_zero_and_negative(self):
        """Test handling of zero and negative values."""
        assert CodeEnum.failed.value == 0
        assert CodeEnum.is_valid_value(0) is True
        assert CodeEnum.get_by_value(0) is CodeEnum.failed

    def test_inheritance_and_instance_checks(self):
        """Test that enum members are proper instances."""
        assert isinstance(CodeEnum.succeeded, CodeEnum)
        assert isinstance(CodeEnum.succeeded, int)
        assert isinstance(CodeEnum.succeeded, BetterIntEnum)
        assert issubclass(CodeEnum, BetterIntEnum)
        assert issubclass(CodeEnum, int)


class TestBetterStrEnum:
    """Comprehensive tests for BetterStrEnum."""

    def test_enum_basic_functionality(self):
        """Test that it still works as a regular string enum."""
        assert StatusEnum.succeeded == "SUCCEEDED"
        assert StatusEnum.failed == "FAILED"

        # Test string operations
        assert StatusEnum.succeeded.lower() == "succeeded"
        assert StatusEnum.succeeded.replace("SUC", "FAIL") == "FAILCEEDED"
        assert len(StatusEnum.succeeded) == 9
        assert StatusEnum.succeeded.startswith("SUC")

        # Test string formatting
        assert f"Status: {StatusEnum.succeeded.value}" == "Status: SUCCEEDED"
        assert "{}".format(StatusEnum.succeeded.value) == "SUCCEEDED"

        # Test collections
        assert {StatusEnum.succeeded, StatusEnum.failed} == {"SUCCEEDED", "FAILED"}
        assert StatusEnum.succeeded in ["SUCCEEDED", "FAILED"]

    def test_get_by_value_success(self):
        assert StatusEnum.get_by_value("SUCCEEDED") is StatusEnum.succeeded
        assert StatusEnum.get_by_value("FAILED") is StatusEnum.failed

    def test_get_by_value_valueerror(self):
        with pytest.raises(ValueError):
            StatusEnum.get_by_value("SUCCESS")  # Wrong value
        with pytest.raises(ValueError):
            StatusEnum.get_by_value("succeeded")  # Wrong case
        with pytest.raises(ValueError):
            StatusEnum.get_by_value("")
        with pytest.raises(ValueError):
            StatusEnum.get_by_value("NONEXISTENT")
        with pytest.raises(ValueError):
            StatusEnum.get_by_value(" SUCCEEDED")  # Leading space
        with pytest.raises(ValueError):
            StatusEnum.get_by_value("SUCCEEDED ")  # Trailing space

    def test_get_by_value_wrong_types(self):
        with pytest.raises((ValueError, TypeError)):
            StatusEnum.get_by_value(1)
        with pytest.raises((ValueError, TypeError)):
            StatusEnum.get_by_value(None)
        with pytest.raises((ValueError, TypeError)):
            StatusEnum.get_by_value([])
        with pytest.raises((ValueError, TypeError)):
            StatusEnum.get_by_value({})

    def test_is_valid_value_success(self):
        assert StatusEnum.is_valid_value("SUCCEEDED") is True
        assert StatusEnum.is_valid_value("FAILED") is True

    def test_is_valid_value_failure(self):
        assert StatusEnum.is_valid_value("SUCCESS") is False
        assert StatusEnum.is_valid_value("succeeded") is False
        assert StatusEnum.is_valid_value("") is False
        assert StatusEnum.is_valid_value("NONEXISTENT") is False
        assert StatusEnum.is_valid_value(" SUCCEEDED") is False
        assert StatusEnum.is_valid_value("SUCCEEDED ") is False
        assert StatusEnum.is_valid_value(1) is False
        assert StatusEnum.is_valid_value(None) is False
        assert StatusEnum.is_valid_value([]) is False
        assert StatusEnum.is_valid_value({}) is False

    def test_ensure_is_valid_value_success(self):
        # Should not raise any exceptions
        StatusEnum.ensure_is_valid_value("SUCCEEDED")
        StatusEnum.ensure_is_valid_value("FAILED")

    def test_ensure_is_valid_value_failure(self):
        with pytest.raises(
            ValueError, match="Invalid `class test_enum_mate.StatusEnum`: 'SUCCESS'"
        ):
            StatusEnum.ensure_is_valid_value("SUCCESS")
        with pytest.raises(
            ValueError, match="Invalid `class test_enum_mate.StatusEnum`: 'succeeded'"
        ):
            StatusEnum.ensure_is_valid_value("succeeded")
        with pytest.raises(
            ValueError, match="Invalid `class test_enum_mate.StatusEnum`: ''"
        ):
            StatusEnum.ensure_is_valid_value("")

    def test_ensure_str_with_str_values(self):
        assert StatusEnum.ensure_str("SUCCEEDED") == "SUCCEEDED"
        assert StatusEnum.ensure_str("FAILED") == "FAILED"

        # Verify return type
        result = StatusEnum.ensure_str("SUCCEEDED")
        assert isinstance(result, str)
        assert type(result) is str

    def test_ensure_str_with_enum_values(self):
        assert StatusEnum.ensure_str(StatusEnum.succeeded) == "SUCCEEDED"
        assert StatusEnum.ensure_str(StatusEnum.failed) == "FAILED"

        # Verify return type
        result = StatusEnum.ensure_str(StatusEnum.succeeded)
        assert isinstance(result, str)
        assert type(result) is str

    def test_ensure_str_invalid_values(self):
        with pytest.raises(ValueError):
            StatusEnum.ensure_str("SUCCESS")
        with pytest.raises(ValueError):
            StatusEnum.ensure_str("succeeded")
        with pytest.raises((ValueError, TypeError)):
            StatusEnum.ensure_str(1)
        with pytest.raises((ValueError, TypeError)):
            StatusEnum.ensure_str(None)

    def test_get_values_multiple(self):
        values = StatusEnum.get_values()
        assert values == ["SUCCEEDED", "FAILED"]
        assert isinstance(values, list)
        assert all(isinstance(val, str) for val in values)

    def test_get_values_single(self):
        values = SingleStrEnum.get_values()
        assert values == ["SINGLE"]

    def test_get_values_empty(self):
        values = EmptyStrEnum.get_values()
        assert values == []

    def test_edge_cases_empty_and_special_chars(self):
        """Test handling of edge case string values."""

        class SpecialStrEnum(BetterStrEnum):
            empty_like = " "
            with_numbers = "VALUE123"
            with_special = "VALUE_WITH-SPECIAL.CHARS"

        assert SpecialStrEnum.is_valid_value(" ") is True
        assert SpecialStrEnum.is_valid_value("VALUE123") is True
        assert SpecialStrEnum.is_valid_value("VALUE_WITH-SPECIAL.CHARS") is True
        assert SpecialStrEnum.get_by_value(" ") is SpecialStrEnum.empty_like

    def test_inheritance_and_instance_checks(self):
        """Test that enum members are proper instances."""
        assert isinstance(StatusEnum.succeeded, StatusEnum)
        assert isinstance(StatusEnum.succeeded, str)
        assert isinstance(StatusEnum.succeeded, BetterStrEnum)
        assert issubclass(StatusEnum, BetterStrEnum)
        assert issubclass(StatusEnum, str)


class TestErrorMessages:
    """Test that error messages are helpful and consistent."""

    def test_int_enum_error_messages(self):
        try:
            CodeEnum.ensure_is_valid_value(999)
        except ValueError as e:
            assert "Invalid `class test_enum_mate.CodeEnum`: 999" in str(e)

        try:
            CodeEnum.ensure_is_valid_value("invalid")
        except ValueError as e:
            assert "Invalid `class test_enum_mate.CodeEnum`: 'invalid'" in str(e)

    def test_str_enum_error_messages(self):
        try:
            StatusEnum.ensure_is_valid_value("invalid")
        except ValueError as e:
            assert "Invalid `class test_enum_mate.StatusEnum`: 'invalid'" in str(e)

        try:
            StatusEnum.ensure_is_valid_value(123)
        except ValueError as e:
            assert "Invalid `class test_enum_mate.StatusEnum`: 123" in str(e)


class TestInteroperability:
    """Test interoperability between different enum types and standard types."""

    def test_int_enum_with_regular_ints(self):
        """Test that BetterIntEnum works with regular integers."""
        value = CodeEnum.succeeded
        regular_int = 1

        assert value == regular_int
        assert value + regular_int == 2
        assert value * regular_int == 1
        assert value in [0, 1, 2]
        assert regular_int in [CodeEnum.failed, CodeEnum.succeeded]

    def test_str_enum_with_regular_strings(self):
        """Test that BetterStrEnum works with regular strings."""
        value = StatusEnum.succeeded
        regular_str = "SUCCEEDED"

        assert value == regular_str
        assert value + "_EXTRA" == "SUCCEEDED_EXTRA"
        assert value.replace("ED", "ING") == "SUCCEINGING"
        assert value in ["SUCCEEDED", "FAILED"]
        assert regular_str in [StatusEnum.succeeded, StatusEnum.failed]

    def test_mixed_operations(self):
        """Test operations mixing enum values with regular values."""
        # Int enum mixed operations
        result1 = CodeEnum.succeeded + 5
        assert result1 == 6
        assert isinstance(result1, int)

        result2 = 10 - CodeEnum.succeeded
        assert result2 == 9
        assert isinstance(result2, int)

        # Str enum mixed operations
        result3 = "PREFIX_" + StatusEnum.succeeded
        assert result3 == "PREFIX_SUCCEEDED"
        assert isinstance(result3, str)

        result4 = StatusEnum.succeeded + "_SUFFIX"
        assert result4 == "SUCCEEDED_SUFFIX"
        assert isinstance(result4, str)


if __name__ == "__main__":
    from enum_mate.tests import run_cov_test

    run_cov_test(
        __file__,
        "enum_mate.impl",
        preview=False,
    )
