import json
from django.core.management.base import BaseCommand, CommandError
from AkvoDjangoFormGateway.models import AkvoGatewayForm as Forms
from AkvoDjangoFormGateway.models import AkvoGatewayQuestion as Questions
from AkvoDjangoFormGateway.models import AkvoGatewayQuestionOption as QO
from AkvoDjangoFormGateway.constants import QuestionTypes


def seed_questions(form: Forms, questions: list):
    for qi, q in enumerate(questions):
        question = Questions.objects.filter(pk=q["id"]).first()
        if not question:
            question = Questions.objects.create(
                id=q["id"],
                form=form,
                order=qi + 1,
                text=q["question"],
                type=getattr(QuestionTypes, q["type"]),
                required=q.get("required"),
            )
        else:
            question.order = q.get("order")
            question.text = q["question"]
            question.type = getattr(QuestionTypes, q["type"])
            question.required = q.get("required")
            question.save()
        if q.get("options"):
            QO.objects.filter(question=question).all().delete()
            QO.objects.bulk_create(
                [
                    QO(
                        name=o["name"].strip(),
                        question=question,
                        order=io + 1,
                    )
                    for io, o in enumerate(q.get("options"))
                ]
            )


def seed_form(form: Forms, data: dict):
    if not form:
        form = Forms.objects.create(
            id=data["id"],
            name=data["form"],
            description=data.get("description"),
            version=1,
        )
    else:
        form.name = data["form"]
        form.description = data.get("description")
        form.version += 1
        form.save()


class Command(BaseCommand):
    help = "Seeder command"

    def add_arguments(self, parser):
        parser.add_argument(
            "-t", "--test", nargs="?", const=1, default=False, type=int
        )
        parser.add_argument("-f", "--file", nargs="?", type=str)

    def handle(self, *args, **options):
        test = options.get("test")
        try:
            JSON_FILE = options.get("file")
            with open(f"{JSON_FILE}") as json_file:
                json_form = json.load(json_file)
            for jf in json_form:
                form = Forms.objects.filter(id=jf["id"]).first()
                seed_form(form=form, data=jf)
                seed_questions(form=Forms, questions=jf["questions"])
            if not test:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully seed from :"%s"' % JSON_FILE
                    )
                )
        except Exception as e:
            raise CommandError(e)
