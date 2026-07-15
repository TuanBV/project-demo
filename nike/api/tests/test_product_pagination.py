"""
Unit tests for ProductService.get_all() pagination/filter wiring.

Mocks only the repository (the external/persistence boundary) — the pagination
math (total_pages) and parameter pass-through are the unit under test.
"""

from product import ProductService


class FakeProductRepository:
    def __init__(self, items, total):
        self.items = items
        self.total = total
        self.get_all_calls = []
        self.count_calls = []

    def get_all(self, page, page_size, category_id, kind_id, name):
        self.get_all_calls.append((page, page_size, category_id, kind_id, name))
        return self.items

    def count_products(self, category_id, kind_id, name):
        self.count_calls.append((category_id, kind_id, name))
        return self.total


def make_service(items=None, total=0):
    repo = FakeProductRepository(items or [], total)
    return ProductService(
        product_repository=repo,
        sale_repository=None,
        image_repository=None,
        category_repository=None,
    ), repo


def test_get_all_computes_total_pages_with_remainder():
    service, repo = make_service(items=[{"product_id": 1}], total=100)

    result = service.get_all(page=2, page_size=12)

    assert result["total"] == 100
    assert result["page"] == 2
    assert result["page_size"] == 12
    assert result["total_pages"] == 9  # ceil(100 / 12)
    assert repo.get_all_calls == [(2, 12, None, None, None)]
    assert repo.count_calls == [(None, None, None)]


def test_get_all_computes_total_pages_on_exact_multiple():
    service, _ = make_service(items=[], total=100)

    result = service.get_all(page=1, page_size=20)

    assert result["total_pages"] == 5


def test_get_all_passes_filters_through_to_repository():
    service, repo = make_service(items=[], total=0)

    service.get_all(page=1, page_size=12, category_id="1", kind_id="2", name="air")

    assert repo.get_all_calls == [(1, 12, "1", "2", "air")]
    assert repo.count_calls == [("1", "2", "air")]


def test_get_all_with_no_matches_returns_zero_total_pages():
    service, _ = make_service(items=[], total=0)

    result = service.get_all(page=1, page_size=12)

    assert result["total"] == 0
    assert result["total_pages"] == 0
