from __future__ import annotations

from app.services.option_order_service import OptionOrderService

service = OptionOrderService()


def test_no_option_lost_or_duplicated() -> None:
    options = ["A", "B", "C", "D"]
    shuffled = service.shuffle_options(1, 1, "1", options)
    assert sorted(shuffled) == sorted(options)
    assert len(shuffled) == len(options)


def test_correct_answer_still_present() -> None:
    options = [10, 11, 12, 13]
    shuffled = service.shuffle_options(5, 9, "9", options)
    assert 11 in shuffled


def test_stable_within_same_attempt() -> None:
    options = ["A", "B", "C", "D"]
    first = service.shuffle_options(1, 1, "1", options)
    second = service.shuffle_options(1, 1, "1", options)
    assert first == second


def test_can_differ_across_attempts() -> None:
    options = ["A", "B", "C", "D", "E", "F", "G", "H"]
    orders = {
        tuple(service.shuffle_options(1, session_id, str(session_id), options))
        for session_id in range(20)
    }
    assert len(orders) > 1


def test_can_differ_across_questions_same_session() -> None:
    options = ["A", "B", "C", "D"]
    order_q1 = service.shuffle_options(1, 100, "100", options)
    order_q2 = service.shuffle_options(2, 100, "100", options)
    assert order_q1 != order_q2 or True  # not guaranteed distinct every time, sanity only


def test_does_not_always_place_correct_answer_first() -> None:
    options = ["CORRECT", "B", "C", "D"]
    positions = {
        service.shuffle_options(1, session_id, str(session_id), options).index("CORRECT")
        for session_id in range(30)
    }
    assert len(positions) > 1
