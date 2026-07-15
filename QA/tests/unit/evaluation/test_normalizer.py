from __future__ import annotations

from app.evaluation.normalizer import TextNormalizer


def test_lowercase() -> None:
    result = TextNormalizer().normalize("HELLO World")
    assert result.with_diacritics == "hello world"


def test_unicode_normalization() -> None:
    decomposed = "é"  # e + combining acute accent
    result = TextNormalizer().normalize(decomposed)
    assert result.with_diacritics == "é"


def test_vietnamese_with_diacritics_preserved() -> None:
    result = TextNormalizer().normalize("Đây là câu trả lời")
    assert "đây" in result.with_diacritics
    assert "câu" in result.with_diacritics


def test_vietnamese_without_diacritics_variant() -> None:
    result = TextNormalizer().normalize("Đây là câu trả lời")
    assert result.without_diacritics == "day la cau tra loi"


def test_keeps_double_equals() -> None:
    result = TextNormalizer().normalize("so sanh a == b")
    assert "==" in result.with_diacritics


def test_keeps_star_args() -> None:
    result = TextNormalizer().normalize("ham foo(*args) nhan tham so bat ky")
    assert "*args" in result.with_diacritics


def test_keeps_double_star_kwargs() -> None:
    result = TextNormalizer().normalize("ham foo(**kwargs) nhan keyword args")
    assert "**kwargs" in result.with_diacritics


def test_keeps_big_o_notation() -> None:
    result = TextNormalizer().normalize("thuat toan chay O(n) thoi gian va O(1) bo nho")
    assert "o(n)" in result.with_diacritics
    assert "o(1)" in result.with_diacritics


def test_big_o_does_not_swallow_function_calls() -> None:
    result = TextNormalizer().normalize("goi ham foo(x, y) de tinh toan")
    assert "foo" in result.with_diacritics.split()


def test_keeps_dunder_init() -> None:
    result = TextNormalizer().normalize("__init__ la constructor cua class")
    assert "__init__" in result.with_diacritics


def test_alias_canonicalization_vietnamese_and_english() -> None:
    vi = TextNormalizer().normalize("day la kieu du lieu bat bien")
    en = TextNormalizer().normalize("this is an immutable type")
    assert "immutable" in vi.with_diacritics
    assert "immutable" in en.with_diacritics


def test_camel_case_split() -> None:
    result = TextNormalizer().normalize("getUserById tra ve user")
    assert "get" in result.tokens
    assert "user" in result.tokens
    assert "by" in result.tokens
    assert "id" in result.tokens


def test_empty_answer_normalizes_to_empty() -> None:
    result = TextNormalizer().normalize("")
    assert result.with_diacritics == ""
    assert result.tokens == []
