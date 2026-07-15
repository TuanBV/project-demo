"""
Regression test for the custom IntEnum SQLAlchemy TypeDecorator.

A LEFT OUTER JOIN to an unmatched row yields NULL for every one of its
columns. Before the fix, process_result_value(None, ...) raised
"ValueError: None is not a valid FlgDelete" — which broke GET /product as
soon as any product existed alongside an empty image table, since the
listing query outer-joins Product -> ProductImage -> Image.
"""

from utils.kbn import IntEnum, FlgDelete


def test_process_result_value_returns_none_for_null_column():
    column_type = IntEnum(FlgDelete)
    assert column_type.process_result_value(None, dialect=None) is None


def test_process_result_value_still_converts_real_values():
    column_type = IntEnum(FlgDelete)
    assert column_type.process_result_value(0, dialect=None) is FlgDelete.OFF
    assert column_type.process_result_value(1, dialect=None) is FlgDelete.ON


def test_process_bind_param_handles_none():
    column_type = IntEnum(FlgDelete)
    assert column_type.process_bind_param(None, dialect=None) is None


def test_process_bind_param_still_converts_real_values():
    column_type = IntEnum(FlgDelete)
    assert column_type.process_bind_param(FlgDelete.ON, dialect=None) == 1
    assert column_type.process_bind_param(1, dialect=None) == 1
