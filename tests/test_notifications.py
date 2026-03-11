def test_send_email_console(client):
    payload = {
        "channel": "email",
        "to": "test@example.com",
        "subject": "Hola",
        "message": "Mensaje de prueba",
    }
    response = client.post("/api/v1/notifications/send", json=payload)

    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert body["provider"] == "console-email"


def test_email_requires_subject(client):
    payload = {
        "channel": "email",
        "to": "test@example.com",
        "message": "Mensaje de prueba",
    }
    response = client.post("/api/v1/notifications/send", json=payload)

    assert response.status_code == 400


def test_send_sms_console(client):
    payload = {
        "channel": "sms",
        "to": "+573001112233",
        "message": "Tu OTP es 123456",
    }
    response = client.post("/api/v1/notifications/send", json=payload)

    assert response.status_code == 200
    body = response.get_json()
    assert body["provider"] == "console-sms"

