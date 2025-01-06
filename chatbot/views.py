import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Sample questions and their predefined API request examples
SAMPLE_QA = {
    "How do I search for people given their current title, current company and location?": {
        "question": "How do I search for people given their current title, current company, and location?",
        "api_request": {
            "url": "https://api.crustdata.com/screener/person/search",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Token $token"
            },
            "data": {
                "filters": [
                    {"filter_type": "CURRENT_COMPANY", "type": "in", "value": ["openai.com"]},
                    {"filter_type": "CURRENT_TITLE", "type": "in", "value": ["engineer"]},
                    {"filter_type": "REGION", "type": "in", "value": ["San Francisco, California, United States"]}
                ],
                "page": 1
            }
        },
        "response": "You can use `api.crustdata.com/screener/person/search` endpoint. Here is an example curl request to find people with title engineer at OpenAI in San Francisco."
    },
    "What is an API?": {
        "question": "What is an API?",
        "response": "API stands for Application Programming Interface. It allows two applications to communicate with each other. APIs are used to request data, send data, or even update systems from one system to another."
    }
}

# Function to validate and execute API request
def validate_and_execute_api_request(api_request):
    try:
        response = requests.request(
            method=api_request["method"],
            url=api_request["url"],
            headers=api_request["headers"],
            json=api_request["data"]
        )

        if response.status_code == 200:
            return response.json()  # Return successful response
        else:
            return {"error": f"API Request failed with status code {response.status_code}", "details": response.text}

    except Exception as e:
        return {"error": f"API request failed due to error: {str(e)}"}

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

            # Check if the user's message matches a predefined question
            qa = SAMPLE_QA.get(user_message, None)

            if qa:
                # If it involves an API request, validate and send the request
                if "api_request" in qa:
                    api_result = validate_and_execute_api_request(qa["api_request"])
                    
                    # Check if the API result contains an error
                    if "error" in api_result:
                        return JsonResponse({
                            'response': f"Sorry, there was an issue with the API request: {api_result['error']}. Here are the details: {api_result.get('details', '')}"
                        }, status=400)
                    else:
                        return JsonResponse({
                            'response': qa["response"] + "\nAPI Request was successful! Here is the result: " + str(api_result)
                        }, status=200)
                else:
                    # Simple non-API-based response
                    return JsonResponse({'response': qa["response"]}, status=200)

            else:
                # Fallback if no predefined answer exists
                return JsonResponse({'response': "I'm sorry, I couldn't understand your question. Please try rephrasing it."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
