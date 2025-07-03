from django.shortcuts import render
import openai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime

openai.api_type = "azure"
openai.api_base = settings.AZURE_OPENAI_ENDPOINT
openai.api_key = settings.AZURE_OPENAI_API_KEY
openai.api_version = "2023-05-15"

class ChatAPIView(APIView):
    def post(self, request):
        user_input = request.data.get("message")
        if not user_input:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = openai.ChatCompletion.create(
                engine=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.9,
                top_p=0.7,
                max_tokens=500
            )

            reply = response.choices[0].message['content']
            model = response.model
            temperature = 0.9
            top_p = 0.7
            tokens_used = response.usage.total_tokens

            return Response({
                "reply": reply,
                "timestamp": datetime.datetime.now().isoformat(),
                "model": model,
                "temperature": temperature,
                "top_p": top_p,
                "tokens_used": tokens_used
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)



def chat_ui(request):
    return render(request, 'brixie/chat.html')
