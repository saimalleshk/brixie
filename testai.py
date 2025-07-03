import openai

# Replace with your actual values
AZURE_OPENAI_ENDPOINT = "https://brixie-resource.cognitiveservices.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview/"
AZURE_OPENAI_API_KEY = "CwihcUBe3zT9PfZ3VDrTaAfKdpkXQAzub4Esh4FPXKcMAn0ct33yJQQJ99BGACHYHv6XJ3w3AAAAACOG9BWo"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_version = "22024-11-20"

def test_openai():
    try:
        response = openai.ChatCompletion.create(
            engine=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, test connection."}
            ],
            max_tokens=50,
            temperature=0.7,
        )
        print("Response from Azure OpenAI:")
        print(response.choices[0].message["content"])
    except Exception as e:
        print("Error during API call:")
        print(e)

if __name__ == "__main__":
    test_openai()
