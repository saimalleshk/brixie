from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from openai import AzureOpenAI
from django.conf import settings
import traceback

# Initialize the AzureOpenAI client once
client = AzureOpenAI(
    api_version="2024-12-01-preview",  # Use your API version here
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,  # Make sure it ends with '/'
    api_key=settings.AZURE_OPENAI_API_KEY,
)

class ChatAPIView(APIView):
    def post(self, request):
        user_input = request.data.get("message")
        if not user_input:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,  # Your deployment/model name
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.9,
                top_p=0.7,
                max_tokens=500,
            )

            reply = response.choices[0].message.content
            model = settings.AZURE_OPENAI_DEPLOYMENT_NAME
            temperature = 0.9
            top_p = 0.7

            tokens_used = None
            if hasattr(response, "usage") and hasattr(response.usage, "total_tokens"):
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
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


def chat_ui(request):
    return render(request, 'brixie/chat.html')
