from pokeagent.api import get_item, get_move


class FakeResponse:
    status_code = 200

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {}


def test_get_move_converts_spaces_to_hyphens(
    monkeypatch,
) -> None:
    requested_urls = []

    def fake_get(url, timeout):
        requested_urls.append(url)
        return FakeResponse()

    monkeypatch.setattr(
        "pokeagent.api.requests.get",
        fake_get,
    )

    get_move("thunder wave")

    assert requested_urls[0].endswith(
        "/move/thunder-wave"
    )


def test_get_item_converts_spaces_to_hyphens(
    monkeypatch,
) -> None:
    requested_urls = []

    def fake_get(url, timeout):
        requested_urls.append(url)
        return FakeResponse()

    monkeypatch.setattr(
        "pokeagent.api.requests.get",
        fake_get,
    )

    get_item("rare candy")

    assert requested_urls[0].endswith(
        "/item/rare-candy"
    )