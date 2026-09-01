from django.urls import reverse


def test_health_check_returns_stable_liveness_payload(client):
    response = client.get(reverse("core:health"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "postgraduate-studies",
    }
    assert (
        response.headers["Cache-Control"]
        == "max-age=0, no-cache, no-store, must-revalidate, private"
    )


def test_health_check_rejects_non_get_requests(client):
    response = client.post(reverse("core:health"))

    assert response.status_code == 405
