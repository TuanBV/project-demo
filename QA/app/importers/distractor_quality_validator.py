"""DistractorQualityValidator: rule-based sanity checks on a 4-option set (spec section 20).

Produces warnings only -- it does not understand semantics, so it flags obvious formal
problems (generic catch-alls, extreme length skew, a distractor that just wraps the correct
answer) rather than judging correctness. Callers decide whether warnings should force
`needs_review`.
"""

from __future__ import annotations

import re

from app.evaluation.normalizer import strip_diacritics

_PUNCTUATION_RE = re.compile(r"[.,;:!?\"'()\[\]{}]")

_GENERIC_PHRASES = {
    "tat ca dap an tren",
    "tat ca cac dap an tren",
    "khong co dap an nao dung",
    "khong co dap an nao",
    "khong dap an nao dung",
    "khong biet",
    "all of the above",
    "none of the above",
    "i don't know",
    "i dont know",
}
_SHORT_RATIO_THRESHOLD = 0.4
_LONG_RATIO_THRESHOLD = 1.6


def _ascii_key(text: str) -> str:
    stripped = _PUNCTUATION_RE.sub(" ", strip_diacritics(text).lower())
    return " ".join(stripped.split())


class DistractorQualityValidator:
    def validate(self, correct_answer: str, distractors: list[str]) -> list[str]:
        warnings: list[str] = []
        lengths = [len(correct_answer)] + [len(d) for d in distractors]
        average_length = sum(lengths) / len(lengths) if lengths else 0

        correct_key = _ascii_key(correct_answer)

        for distractor in distractors:
            key = _ascii_key(distractor)
            if key in _GENERIC_PHRASES:
                warnings.append(f"Đáp án sai quá chung chung, dễ đoán: '{distractor}'")
            if average_length and len(distractor) < average_length * _SHORT_RATIO_THRESHOLD:
                warnings.append(
                    f"Đáp án sai ngắn hơn hẳn các đáp án khác, có thể lộ đáp án: '{distractor}'"
                )
            if correct_key and key != correct_key and correct_key in key:
                warnings.append(
                    f"Đáp án sai chứa toàn bộ đáp án đúng, dễ gây nhầm lẫn: '{distractor}'"
                )

        if average_length and len(correct_answer) > average_length * _LONG_RATIO_THRESHOLD:
            warnings.append("Đáp án đúng dài vượt trội so với các đáp án sai, có thể làm lộ đáp án")

        seen_keys: dict[str, str] = {}
        for distractor in distractors:
            key = _ascii_key(distractor)
            if key in seen_keys:
                warnings.append(f"Hai đáp án sai trùng nội dung: '{distractor}'")
            seen_keys[key] = distractor

        return warnings
