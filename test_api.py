import pytest
import allure
import requests
from unittest.mock import patch, Mock

from api import (
    get_products,
    search_products,
    get_product_by_id,
    add_product,
)


@allure.epic("DummyJSON API")
@allure.feature("Products")
class TestProducts:

    @allure.story("Get products")
    @allure.title("Получение списка продуктов по умолчанию")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products(self):
        data = get_products()
        assert "products" in data

    @allure.story("Get products")
    @allure.title("Граничные значения: limit=100, skip=0")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_boundaries(self):
        data = get_products(limit=100, skip=0)
        assert len(data["products"]) <= 100

    @allure.story("Get products")
    @pytest.mark.parametrize("limit", [0, 101])
    @allure.title("Некорректный limit={limit}")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_products_invalid_limit(self, limit):
        with pytest.raises(ValueError):
            get_products(limit=limit)

    @allure.story("Get products")
    @allure.title("Некорректный skip=-1")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_products_invalid_skip(self):
        with pytest.raises(ValueError):
            get_products(skip=-1)

    @allure.story("Search products")
    @allure.title("Поиск продуктов по запросу phone")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_products(self):
        data = search_products("phone")
        assert len(data["products"]) > 0

    @allure.story("Search products")
    @pytest.mark.parametrize("query", ["", "   "])
    @allure.title("Пустой/пробельный поисковый запрос: {query!r}")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_products_empty_query(self, query):
        with pytest.raises(ValueError):
            search_products(query)

    @allure.story("Search products")
    @allure.title("Некорректный limit при поиске")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_products_invalid_limit(self):
        with pytest.raises(ValueError):
            search_products("phone", limit=0)

    @allure.story("Get product by ID")
    @allure.title("Получение продукта по ID=1")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_product_by_id(self):
        data = get_product_by_id(1)
        assert data["id"] == 1

    @allure.story("Get product by ID")
    @allure.title("Получение несуществующего продукта возвращает None")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_product_by_id_not_found(self):
        response = Mock()
        response.status_code = 404

        with patch("api.requests.get", return_value=response):
            assert get_product_by_id(999999) is None

    @allure.story("Get product by ID")
    @pytest.mark.parametrize("product_id", ["1", 0, -5])
    @allure.title("Некорректный product_id={product_id!r}")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_product_by_id_invalid(self, product_id):
        with pytest.raises(ValueError):
            get_product_by_id(product_id)

    @allure.story("Add product")
    @allure.title("Добавление продукта")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_product(self):
        data = add_product("Test Phone", 999)
        assert data["title"] == "Test Phone"

    @allure.story("Add product")
    @pytest.mark.parametrize(
        "title, price",
        [
            ("", 100),
            (None, 100),
            ("Valid", 0),
            ("Valid", -1),
        ],
    )
    @allure.title("Валидация add_product: title={title!r}, price={price}")
    @allure.severity(allure.severity_level.MINOR)
    def test_add_product_validation(self, title, price):
        with pytest.raises(ValueError):
            add_product(title, price)

    @allure.story("HTTP errors")
    @allure.title("HTTP-ошибка при получении продуктов пробрасывается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_products_http_error(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("500")

        with patch("api.requests.get", return_value=response):
            with pytest.raises(requests.HTTPError):
                get_products()

    @allure.story("HTTP errors")
    @allure.title("HTTP-ошибка при добавлении продукта пробрасывается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_product_http_error(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("500")

        with patch("api.requests.post", return_value=response):
            with pytest.raises(requests.HTTPError):
                add_product("Phone", 100)