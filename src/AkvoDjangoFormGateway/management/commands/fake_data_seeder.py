from datetime import datetime, timedelta, time
from faker import Faker

from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware
from AkvoDjangoFormGateway.models import AkvoGatewayForm as Forms
from AkvoDjangoFormGateway.models import AkvoGatewayData as FormData
from AkvoDjangoFormGateway.models import AkvoGatewayAnswer as Answers
from AkvoDjangoFormGateway.constants import QuestionTypes

fake = Faker()


def set_answer_data(data, question):
    name = None
    value = None
    option = None

    if question.type == QuestionTypes.geo:
        option = data.geo
    elif question.type == QuestionTypes.text:
        name = fake.sentence(nb_words=3)
    elif question.type == QuestionTypes.number:
        value = fake.random_int(min=10, max=50)
    elif question.type == QuestionTypes.option:
        option = [
            question.ag_question_question_options.order_by('?').first().name
        ]
    elif question.type == QuestionTypes.multiple_option:
        option = list(
            question.ag_question_question_options.order_by('?').values_list(
                'name', flat=True
            )[0 : fake.random_int(min=1, max=3)]
        )
    elif question.type == QuestionTypes.photo:
        name = fake.image_url()
    elif question.type == QuestionTypes.date:
        name = fake.date_between_dates(
            date_start=timezone.datetime.now().date() - timedelta(days=90),
            date_end=timezone.datetime.now().date(),
        ).strftime("%m/%d/%Y")
    else:
        pass
    return name, value, option


def add_fake_answers(data: FormData):
    form = data.form
    for question in form.ag_form_questions.all():
        name, value, option = set_answer_data(data, question)
        Answers.objects.create(
            data=data,
            question=question,
            name=name,
            value=value,
            options=option,
        )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-r", "--repeat", nargs="?", const=20, default=20, type=int
        )
        parser.add_argument(
            "-t", "--test", nargs="?", const=False, default=False, type=bool
        )

    def handle(self, *args, **options):
        test = options.get("test")
        repeat = options.get("repeat")
        FormData.objects.all().delete()
        for form in Forms.objects.all():
            if not test:
                print(f"\nSeeding - {form.name}")
            for i in range(repeat):
                now_date = datetime.now()
                start_date = now_date - timedelta(days=5 * 365)
                created = fake.date_between(start_date, now_date)
                created = datetime.combine(created, time.min)
                lat = fake.latitude()
                lng = fake.longitude()
                geo_value = f"{lat},{lng}"
                data = FormData.objects.create(
                    form=form,
                    name=fake.pystr_format(),
                    phone=fake.phone_number(),
                    geo=geo_value,
                )
                data.created = make_aware(created)
                data.save()
                add_fake_answers(data)
