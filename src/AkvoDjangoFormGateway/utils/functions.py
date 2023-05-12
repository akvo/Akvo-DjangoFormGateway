from AkvoDjangoFormGateway.models import AkvoGatewayAnswer
from AkvoDjangoFormGateway.constants import QuestionTypes


def get_answer_value(answer: AkvoGatewayAnswer, toString: bool = False):
    if answer.question.type in [
        QuestionTypes.geo,
        QuestionTypes.option,
        QuestionTypes.multiple_option,
    ]:
        if toString:
            if answer.options:
                return "|".join([str(a) for a in answer.options])
            return None
        return answer.options
    elif answer.question.type == QuestionTypes.number:
        return answer.value
    elif answer.question.type == QuestionTypes.administration:
        return int(float(answer.value))
    else:
        return answer.name
