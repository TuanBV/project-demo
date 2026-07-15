"""Builds human-readable Vietnamese feedback from evaluation results (template-based, no LLM)."""

from __future__ import annotations

from app.evaluation.base import ContradictionHit, MatchedConcept, MissingConcept


class FeedbackBuilder:
    def build(
        self,
        matched: list[MatchedConcept],
        partial: list[MatchedConcept],
        missing: list[MissingConcept],
        contradictions: list[ContradictionHit],
        classification: str,
    ) -> str:
        parts: list[str] = []

        if matched:
            names = ", ".join(m.name for m in matched)
            parts.append(f"Bạn đã nêu đúng: {names}.")

        if partial:
            names = ", ".join(m.name for m in partial)
            parts.append(f"Bạn đã đề cập nhưng chưa đầy đủ: {names}.")

        if missing:
            names = ", ".join(m.name for m in missing)
            parts.append(f"Bạn còn thiếu các ý: {names}.")

        if contradictions:
            descriptions = "; ".join(c.description for c in contradictions)
            parts.append(f"Phát hiện phát biểu có thể chưa chính xác: {descriptions}.")

        if not matched and not partial and not missing and not contradictions:
            parts.append("Không thể xác định nội dung câu trả lời, vui lòng xem đáp án tham khảo.")

        classification_labels = {
            "CORRECT": "Chính xác",
            "MOSTLY_CORRECT": "Đa phần chính xác",
            "PARTIALLY_CORRECT": "Đúng một phần",
            "INCORRECT": "Chưa chính xác",
        }
        label = classification_labels.get(classification, classification)
        parts.append(f"Đánh giá tổng thể: {label}.")

        return " ".join(parts)
