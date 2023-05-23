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

        json_form = {"From": f"whatsapp:+{phone_number}"}
        response = client.post(
            f"/api/gateway/twilio/{form_id}?format=json", json_form
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # first question shown
        fq = Questions.objects.filter(form=form_id).order_by("order").first()
        self.assertEqual(response.json(), f"{fq.order}. {fq.text}")

        reply_text = "answer first question"
        json_form = {"Body": reply_text, "From": f"whatsapp:+{phone_number}"}

        response = client.post(f"/api/gateway/twilio/{form_id}", json_form)
        datapoint = feed.get_draft_datapoint(phone=phone_number)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            feed.validate_answer(text=reply_text, question=fq, data=datapoint),
            True,
        )
        # Photo question
        print("form", datapoint.form)
        question = feed.get_question(form=datapoint.form, data=datapoint)
        self.assertEqual(response.json(), f"{question.order}. {question.text}")

        # Answer wrong photo question no MediaContentType0
        image = "http://twilio.example/image/caseSensiT1Ve2.png"
        json_form = {
            "Body": "",
            "From": f"whatsapp:+{phone_number}",
            "MediaUrl0": image,
        }
        response = client.post("/api/gateway/twilio/", json_form)
        serializer = TwilioSerializer(data=json_form)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "MediaContentType0 is required when MediaUrl0 is present."
                ]
            },
        )

        image_type = "image/png"
        json_form = {
            "Body": "",
            "From": f"whatsapp:+{phone_number}",
            "MediaContentType0": image_type,
        }
        response = client.post("/api/gateway/twilio/", json_form)
        serializer = TwilioSerializer(data=json_form)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "MediaUrl0 is required when MediaContentType0 is present."
                ]
            },
        )

        # Answer right photo question
        json_form = {
            "Body": "",
            "From": f"whatsapp:+{phone_number}",
            "MediaContentType0": image_type,
            "MediaUrl0": image,
        }
        response = client.post("/api/gateway/twilio/", json_form)
        stored_image = Answers.objects.filter(question=question).first().name
        self.assertEqual(image, stored_image)
        self.assertNotEqual(image.lower(), stored_image)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            feed.validate_answer(
                text="",
                question=question,
                data=datapoint,
                image_type=image_type,
            ),
            True,
        )

        # GPS question
        question = feed.get_question(form=datapoint.form, data=datapoint)

        # Answer Wrong GPS question
        lat = "-7.1161"
        json_form = {
            "Body": "",
            "From": f"whatsapp:+{phone_number}",
            "Latitude": lat,
        }
        text = feed.get_answer_text(
            body=None,
            image_url=None,
            lat=lat,
        )
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        lng = "103.11"
        json_form = {
            "Body": "",
            "From": f"whatsapp:+{phone_number}",
            "Longitude": lng,
        }
        text = feed.get_answer_text(
            body=None,
            image_url=None,
            lng=lng,
        )
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Answer GPS question
        json_form = {
            "Body": "",
            "From": f"whatsapp:+{phone_number}",
            "Latitude": lat,
            "Longitude": lng,
        }
        text = feed.get_answer_text(
            body=None,
            image_url=None,
            lat=lat,
            lng=lng,
        )
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            feed.validate_answer(
                text=text,
                question=question,
                data=datapoint,
            ),
            True,
        )

        # Phone question
        question = feed.get_question(form=datapoint.form, data=datapoint)
        # Answer Phone question
        reply_text = "62819111"
        json_form = {
            "Body": reply_text,
            "From": f"whatsapp:+{phone_number}",
        }
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            feed.validate_answer(
                text=reply_text,
                question=question,
                data=datapoint,
            ),
            True,
        )

        # Single option question
        question = feed.get_question(form=datapoint.form, data=datapoint)
        # Answer Single option question
        reply_text = "OptiOn 2"
        json_form = {
            "Body": reply_text,
            "From": f"whatsapp:+{phone_number}",
        }
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            feed.validate_answer(
                text=reply_text,
                question=question,
                data=datapoint,
            ),
            True,
        )

        # Multiple option question
        question = feed.get_question(form=datapoint.form, data=datapoint)
        # Answer Multiple option question
        reply_text = "multi 1, MULTI 3"
        json_form = {
            "Body": reply_text,
            "From": f"whatsapp:+{phone_number}",
        }
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            feed.validate_answer(
                text=reply_text,
                question=question,
                data=datapoint,
            ),
            True,
        )
        answer = Answers.objects.filter(
            data=datapoint, question=question
        ).first()
        self.assertEqual(answer.options, ["multi 1", "multi 3"])

        # Date question
        question = feed.get_question(form=datapoint.form, data=datapoint)

        # Answer wrong date question
        reply_text = "15/12/1999"
        json_form = {
            "Body": reply_text,
            "From": f"whatsapp:+{phone_number}",
        }
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            feed.validate_answer(
                text=reply_text, question=question, data=datapoint
            )
        )
        # Answer date question
        reply_text = "15-12-1999"
        json_form = {
            "Body": reply_text,
            "From": f"whatsapp:+{phone_number}",
        }
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            feed.validate_answer(
                text=reply_text,
                question=question,
                data=datapoint,
            ),
            True,
        )
        answer = Answers.objects.filter(
            data=datapoint, question=question
        ).first()
        self.assertEqual(answer.name, reply_text)
        self.assertEqual(response.json(), "Thank you!")
