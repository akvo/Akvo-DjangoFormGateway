from django.test import TestCase, Client
from django.core.management import call_command
from rest_framework import status
from AkvoDjangoFormGateway.feed import Feed
from AkvoDjangoFormGateway.models import (
    AkvoGatewayQuestion as Questions,
    AkvoGatewayAnswer as Answers,
)
from AkvoDjangoFormGateway.serializers import TwilioSerializer

client = Client()
feed = Feed()
# Tests
# consider that 8 digit phone number will
# skip to send twillio message
phone_number = "12345678"


class TwilioInstanceEndpointTestCase(TestCase):
    def setUp(self):
        call_command(
            "gateway_form_seeder",
            "-f",
            "./backend/source/forms/1.json",
            "-t",
            True,
        )

    def test_instance_not_found(self):
        form_id = 12345678
        response = client.post(
            f"/api/gateway/twilio/{form_id}?format=json",
            data={},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.json(),
            {"detail": "Not found."},
        )

    def test_instance_request(self):
        form_id = 1
        # Send hi as first message
        reply_text = "hi"
        response = client.post(
            f"/api/gateway/twilio/{form_id}?format=json",
            {"From": f"whatsapp:+{phone_number}", "Body": reply_text},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # No welcome message and select forms
        self.assertNotEqual(response.json(), feed.get_list_form())

        # Got the first question
        fq = Questions.objects.filter(form=form_id).order_by("order").first()
        self.assertEqual(response.json(), f"{fq.order}. {fq.text}")

        # Survey session is created
        datapoint = feed.get_draft_datapoint(phone=phone_number)

        # Answer first question
        reply_text = "test complaint"
        response = client.post(
            f"/api/gateway/twilio/{form_id}",
            {"Body": reply_text, "From": f"whatsapp:+{phone_number}"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            feed.validate_answer(text=reply_text, question=fq, data=datapoint),
            True,
        )
        # Show next question
        question = feed.get_question(form=datapoint.form, data=datapoint)
        self.assertEqual(response.json(), f"{question.order}. {question.text}")
