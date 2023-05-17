from django.conf import settings
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    AkvoGatewayForm as Forms,
    AkvoGatewayData as FormData,
)
from .serializers import ListFormSerializer, TwilioSerializer
from .constants import StatusTypes
from .feed import Feed


@permission_classes([AllowAny])
class CheckView(APIView):
    def get(self, request):
        return Response({"message": settings.TWILIO_ACCOUNT_SID})


class AkvoFormViewSet(ModelViewSet):
    serializer_class = ListFormSerializer
    queryset = Forms.objects.all()


class TwilioViewSet(ViewSet):
    http_method_names = ["post"]

    def create(self, request):
        serializer = TwilioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data["answer"]
        phone = serializer.validated_data["phone"]
        feed = Feed()

        init, form_id = feed.get_init_survey_session(text=text)
        datapoint = feed.get_draft_datapoint(phone=phone)
        survey = feed.get_form(form_id=form_id, data=datapoint)
        lq = feed.get_question(form=survey, data=datapoint)

        if text in feed.welcome and not datapoint:
            message = feed.get_list_form()
            return Response(message)

        if init and not datapoint:
            dp_name = f"{survey.id}-{phone}"
            # create new survey session by creating new datapoint
            FormData.objects.create(
                form=survey,
                name=dp_name,
                phone=phone,
                status=StatusTypes.draft,
            )
            message = f"{lq.order}. {lq.text}"
            return Response(message)

        if datapoint and lq:
            valid_answer = feed.validate_answer(
                text=text, question=lq, data=datapoint
            )
            if valid_answer:
                feed.insert_answer(text=text, question=lq, data=datapoint)
                nq = feed.get_last_question(data=datapoint)
                if nq:
                    # show next question
                    message = f"{nq.order}. {nq.text}"
                else:
                    feed.set_as_completed(data=datapoint)
                    message = "Thank you!"
            else:
                message = f"{lq.order}. {lq.text}"
            return Response(message)
