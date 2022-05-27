from django.http import JsonResponse
from django.views.generic.edit import FormView

from portal.views.chat_bot.chat import handle_question


class Chatbot(FormView):
    def get(self, request, question):
        ans = handle_question(question)
        return JsonResponse({question: ans})
