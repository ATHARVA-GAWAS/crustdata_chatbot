from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

SAMPLE_QA = {
    "How do I search for people given their current title, current company and location?": (
        "You can use `api.crustdata.com/screener/person/search` endpoint. "
        "Here is an example curl request to find people with title engineer at OpenAI in San Francisco:\n\n"
        "```\n"
        "curl --location 'https://api.crustdata.com/screener/person/search' \\\n"
        "--header 'Content-Type: application/json' \\\n"
        "--header 'Authorization: Token $token' \\\n"
        "--data '{\n"
        "    \"filters\": [\n"
        "        {\"filter_type\": \"CURRENT_COMPANY\", \"type\": \"in\", \"value\": [\"openai.com\"]},\n"
        "        {\"filter_type\": \"CURRENT_TITLE\", \"type\": \"in\", \"value\": [\"engineer\"]},\n"
        "        {\"filter_type\": \"REGION\", \"type\": \"in\", \"value\": [\"San Francisco, California, United States\"]}\n"
        "    ],\n"
        "    \"page\": 1\n"
        "}'\n"
        "```"
    ),
    "I tried using the screener/person/search API to compare against previous values this weekend. I am blocked on the filter values.": (
        "Yes, there is a specific list of regions listed here: "
        "[Crustdata Regions](https://crustdata-docs-region-json.s3.us-east-2.amazonaws.com/updated_regions.json). "
        "Is there a way you can find the region from this list first and then put the exact values in the search?"
    ),
}


# View to render chatbot page
def chatbot_page(request):
    return render(request, 'chatbot/index.html')

# View to handle chatbot queries
@csrf_exempt  # Disable CSRF for simplicity in this demo
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            # Match sample questions
            response = SAMPLE_QA.get(user_message, None)

            if response:
                return JsonResponse({'response': response}, status=200)

            # Default fallback response
            return JsonResponse({'response': "I'm sorry, I couldn't understand your question. Please try rephrasing it."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)