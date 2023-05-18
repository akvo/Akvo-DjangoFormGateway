from django.test import TestCase, Client
from django.core.management import call_command
from AkvoDjangoFormGateway.feed import Feed

client = Client()
feed = Feed()


class TwilioEndpointTestCase(TestCase):
    def setUp(self):
        call_command(
            "form_seeder", "-f", "./backend/source/forms/1.json", "-t", True
        )

    def test_request_type(self):
        # GET not allowed
        response = client.get("/api/gateway/twilio/")
        self.assertEqual(response.status_code, 405)

        # POST allowed
        response = client.post("/api/gateway/twilio/")
        self.assertEqual(response.status_code, 200)

    def test_welcome_message(self):
        json_form = {"Body": "hi", "From": "whatsapp:+628139350491"}
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), feed.get_list_form())

    def test_start_survey_session(self):
        reply_text = "ready#1"

        init, form_id = feed.get_init_survey_session(text=reply_text)
        json_form = {"Body": reply_text, "From": "whatsapp:+628139350491"}
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, 200)

        datapoint = feed.get_draft_datapoint(phone="628139350491")
        survey = feed.get_form(form_id=form_id, data=datapoint)
        # First question
        question = feed.get_question(form=survey)
        self.assertEqual(response.json(), f"{question.order}. {question.text}")

        # datapoint is exist
        self.assertEqual(datapoint.phone, "628139350491")
        # Form id equal with datapoint
        self.assertEqual(survey.id, datapoint.form.id)

        # Answer First question
        reply_text = "text answer"
        json_form = {"Body": reply_text, "From": "whatsapp:+628139350491"}
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, 200)

        # Photo question
        question = feed.get_question(form=survey, data=datapoint)
        self.assertEqual(response.json(), f"{question.order}. {question.text}")

        # Answer photo question
        image = "http://twilio.example/image.png"
        image_type = "image/png"
        json_form = {
            "Body": "",
            "From": "whatsapp:+628139350491",
            "MediaContentType0": image_type,
            "MediaUrl0": image,
        }
        response = client.post("/api/gateway/twilio/", json_form)
        self.assertEqual(response.status_code, 200)
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
        question = feed.get_question(form=survey, data=datapoint)

        # Answer GPS question
        lat = "-9.1161"
        lng = "10.11"
        json_form = {
            "Body": "",
            "From": "whatsapp:+628139350491",
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            feed.validate_answer(
                text=text,
                question=question,
                data=datapoint,
            ),
            True,
        )
