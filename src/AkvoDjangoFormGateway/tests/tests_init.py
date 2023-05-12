from django.test import TestCase, Client
from django.conf import settings


class OkEndpointTestCase(TestCase):
    def test_ok_endpoint(self):
        client = Client()
        response = client.get("/api/gateway/check/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"message": settings.TWILIO_ACCOUNT_SID}
        )
