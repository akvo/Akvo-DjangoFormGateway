from datetime import datetime
from .models import (
    AkvoGatewayForm as Forms,
    AkvoGatewayData as FormData,
    AkvoGatewayAnswer as Answers,
    AkvoGatewayQuestion as Questions,
)
from .constants import QuestionTypes, StatusTypes
from .utils.validation import (
    is_number,
    is_alphanumeric,
    is_date,
    is_valid_geolocation,
    is_image_string,
)


class Feed:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.welcome = ["hi", "hello", "info"]

    def get_init_survey_session(self, text: str):
        init = False
        form_id = None
        if "#" in text:
            info = str(text).split("#")
            form_id = info[1]
            init = len(info) == 2 and "READY" in text
        return init, form_id

    def get_form(self, form_id: int = None, data: FormData = None) -> Forms:
        survey = None
        if data:
            survey = data.form
        if form_id:
            survey = Forms.objects.get(pk=form_id)
        return survey

    def get_last_question(self, data: FormData) -> Questions:
        if data.form.ag_form_questions.count() == data.ag_data_answer.count():
            # Return null if all questions are answered
            return None
        aws = data.ag_data_answer.all()
        ids = [aw.question.id for aw in aws]
        qs = (
            data.form.ag_form_questions.exclude(id__in=ids)
            .order_by("order")
            .first()
        )
        return qs

    def get_question(
        self, form: Forms = None, data: FormData = None
    ) -> Questions:
        qs = None
        if form:
            qs = form.ag_form_questions.all().first()
        if data and data.ag_data_answer.count():
            qs = self.get_last_question(data=data)
        return qs

    def get_draft_datapoint(self, phone: str) -> FormData:
        datapoint = (
            FormData.objects.filter(phone=phone, status=StatusTypes.draft)
            .all()
            .first()
        )
        return datapoint

    def get_list_form(self) -> str:
        forms = Forms.objects.all()
        msg = "Welcome to Akvo Survey\n\n."
        msg += "*Please select the form below:*\n"
        for f in forms:
            msg += f"- #{f.id} | {f.name}\n"
        msg += (
            "by replying to this message with the following format to start a"
            " new survey\n"
        )
        msg += "*READY#FORM_ID* (e.g *READY#1*)"
        return msg

    def validate_answer(
        self, text: str, question: Questions, data: FormData
    ) -> None:
        # is alphanumeric by default
        is_valid = is_alphanumeric(input=text)
        if question.type == QuestionTypes.number:
            is_valid = is_number(input=text)
        if question.type == QuestionTypes.date:
            is_valid = is_date(input=text)
        if question.type == QuestionTypes.geo:
            is_valid = is_valid_geolocation(json_string=text)
        if question.type == QuestionTypes.photo:
            is_valid = is_image_string(image_string=text)
        return is_valid

    def insert_answer(self, text: str, question: Questions, data: FormData):
        name = None
        value = None
        options = None
        if question.type == QuestionTypes.number:
            value = text
        if question.type == QuestionTypes.geo:
            options = text
        if question.type == QuestionTypes.date:
            dv = datetime.strptime(text)
            name = dv.strftime("%m/%d/%Y")
        if not name and not value and not options:
            name = text
        return Answers.objects.create(
            question=question,
            data=data,
            name=name,
            value=value,
            options=options,
        )

    def set_as_completed(self, data: FormData) -> None:
        data.status = StatusTypes.submitted
        data.save()
