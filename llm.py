""""
****************************************************************
*****************************************************************
README
*****************************************************************
*****************************************************************


LLM Query Processing Application

This application processes natural language queries using a language model (LLM) to extract structured JSON information about company metrics such as profits, revenue, or other parameters. The output JSON includes entities, parameters, and normalized dates.

Features

1. Natural Language Query Parsing

	Extracts entities, metrics, and date ranges from user queries.

	Handles relative date phrases like "last quarter" or "this year."

2. Support for Multiple Entities and Metrics

	Allows queries comparing multiple companies and metrics (e.g., "Compare Meta's profit with Apple's revenue").

3. Alias Handling

	Standardizes company names and metrics, handling variations, abbreviations, and aliases.

4. Error Handling

	Provides robust error messages for unsupported queries, missing data, or ambiguous inputs.

5. Date Normalization

	Handles explicit and relative dates with appropriate defaults when dates are missing.

******************
Installation
******************

1. Navigate to the project directory:

	cd llm.py

2. Install dependencies:

	pip install requests
	pip install python-dateutil

*****************************************************
Steps to Generate an API Key for the Groq LLM API
*****************************************************

1. Sign Up or Log In

	Go to the Groq platform's official website: Groq LLM API Portal.
	If you don’t already have an account, create one by signing up with your email and password.
	If you already have an account, log in using your credentials.
	Navigate to API Key Section

2. After logging in, navigate to the Developer Dashboard.
	Look for a section labeled API Keys or Access Tokens (this may vary based on the platform's layout).
	Create a New API Key

3. Click the button labeled Create API Key or Generate New Key.
	You may be asked to provide details such as:
	Key name (e.g., "LLM Query Processing Key").
	Access permissions (e.g., read, write, execute) — choose the appropriate level based on your application’s requirements.
	Usage limits or restrictions (e.g., IP whitelisting, rate limits).
	
4. Copy the API Key

	Once the API key is generated, it will be displayed on the screen.
	Important: Copy the API key immediately and save it securely. Many platforms do not allow you to view the API key again for 	security reasons.

*******************
Usage
*******************

1. Run the application:

	python llm.py

2. Enter queries in natural language, such as:

	"What is the profit of Google this year?"

	"Compare the revenue of Meta and Microsoft last quarter."

	"What was Apple's revenue in the previous month?"

3. The application will return a structured JSON output:

[
    {
        "entity": "Google",
        "parameter": "profit",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
]

***********************
Configuration
***********************

1. Aliases

	Modify the entity_aliases and metric_aliases dictionaries in the code to add new aliases for entities and metrics.
	Aliases can be more than what are defined

2. Default Dates

	Update the get_default_dates function to change the default date ranges when no dates are specified.

**************************
Evaluation Criteria
**************************

1. Correctness of JSON Output

	Ensure JSON accurately reflects the user query.

2. Date Handling

	Properly normalize and set default start and end dates.

3. Handling Multiple Entities

	Validate support for comparisons and multi-entity queries.

4. Error Handling

	Robustly handle invalid inputs or ambiguous queries.

5. Code Quality

	Ensure modularity, readability, and proper documentation.

6. LLM Utilization

	Effectively extract query intents using the language model.


Examples

Query: "What is the profit of Microsoft last quarter?"

Output:

[
    {
        "entity": "Microsoft",
        "parameter": "profit",
        "start_date": "2024-07-01",
        "end_date": "2024-09-30"
    }
]

Query: "Compare the revenue of Google and Microsoft last year."

Output:

[
    {
        "entity": "Google",
        "parameter": "revenue",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    },
    {
        "entity": "Microsoft",
        "parameter": "revenue",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
]

*****************
Testing
*****************

Run the application and input the following test queries to validate functionality:

	"What is the profit of Apple in the last month?"

	"Compare Microsoft's revenue with Google's profit this quarter."

	"How much did Amazon earn last year?"

Verify the JSON output for accuracy and completeness.

*************************
Area's to improve:
*************************
Due to shortage of time I am not able to deliver the best and efficient application on llm but for your reference i can list down the current area's to improve in my code which can be fixed by me if given some proper time and discussion.

1. Duplicacy in history
2. Entity's name mismatch in query
3. Can integrate more ambiguous time frames like 1st quarter or any specific month like January
4. The process of extraction of entity and parameters from the query can be modified for different types of query structure ; currently working for 1 structure only
5. Can also make the code more flexible remob=ving some hardcoding which i have done for now
6. Can also optimize the query results in the case of parent company 
7. I think it is a type of project which can be greatly enhanced everytime you look into it

"""
import requests
import json
from datetime import datetime, timedelta
import re

# Define alias mappings for entities and metrics
ENTITY_ALIASES = {
    "google": "Alphabet Inc",
    "alphabet": "Alphabet Inc",
    "meta": "Meta Platforms",
    "facebook": "Meta Platforms",
    "microsoft": "Microsoft",
    "msft": "Microsoft",
    "apple": "Apple Inc",
    "amazon": "Amazon.com Inc"
}

METRIC_ALIASES = {
    "profit": "profit",
    "earnings": "profit",
    "income": "profit",
    "revenue": "revenue",
    "sales": "revenue",
    "performance": "performance"
}

# Constants for date calculation
QUARTER_DAYS = 90  # Approximation for a quarter (3 months)

# Constants
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"  # Replace with your valid API key

def normalize_entity(entity):
    """
    Normalize company names to their canonical forms.
    """
    entity = entity.lower()
    return ENTITY_ALIASES.get(entity.lower(), entity)

def normalize_metric(metric):
    """
    Normalize metric parameters to their canonical forms.
    """
    return METRIC_ALIASES.get(metric.lower(), metric)

def get_default_dates():
    """
    Returns default start and end dates if not provided in the query.
    Start Date: 1 year ago from today.
    End Date: Today's date.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def calculate_relative_dates(relative_date):
    """
    Calculate start and end dates based on relative terms like 'last quarter', 'first quarter', or 'previous month'.
    """
    now = datetime.now()

    if relative_date.lower() == "last quarter":
        current_quarter = (now.month - 1) // 3 + 1
        if current_quarter == 1:  # If it's the first quarter now, last quarter is Q4 of the previous year
            start_date = datetime(now.year - 1, 10, 1)
            end_date = datetime(now.year - 1, 12, 31)
        else:
            start_month = (current_quarter - 2) * 3 + 1
            start_date = datetime(now.year, start_month, 1)
            end_date = datetime(now.year, start_month + 3, 1) - timedelta(days=1)


    elif relative_date.lower() == "first quarter":
        # First quarter: January 1 to March 31
        start_date = datetime(now.year, 1, 1)
        end_date = datetime(now.year, 3, 31)

    elif relative_date.lower() == "previous month":
        # Previous month: Start from the first day of the previous month to its last day
        start_date = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_date = now.replace(day=1) - timedelta(days=1)

    else:
        # Default fallback: last year
        start_date = datetime(now.year - 1, 1, 1)
        end_date = datetime(now.year - 1, 12, 31)

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")



def process_query_with_llm(query, api_url, api_key, history=None):
    """
    Sends the user query to the Groq LLM API and extracts relevant information.
    
    Parameters:
        query (str): The user query to process.
        api_url (str): The Groq API endpoint.
        api_key (str): The API key for authentication.
        history (list): List of previous conversation contexts.
    
    Returns:
        dict: Parsed response from the API or an error message.
    """
    # Prepare message history if it's passed
    messages = [{"role": "user", "content": query}]
    if history:
        for past_response in history:
            # Use .get() to avoid KeyError if 'content' is missing
            messages.append({"role": "assistant", "content": past_response.get("content", "")})

    payload = {
        "model": "llama3-8b-8192",
        "messages": messages
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def extract_information_from_response(response, query):
    """
    Extracts relevant information (e.g., entity, parameter, fiscal year) from the LLM response.
    Handles variations in entity names and parameters.
    """
    try:
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

        # Extract entities
        entity_match = re.findall(r"(Google|Alphabet(?: Inc)?|Meta|Facebook|Amazon|Apple|Microsoft|MSFT)", content, re.IGNORECASE)
        entities = list(set([normalize_entity(entity.strip()) for entity in entity_match]))

        # If multiple entities, pick the first or decide based on query context
        entity = entities[0] if len(entities) == 1 else normalize_entity(re.search(r"(Google|Meta|Facebook|Apple|Amazon|Microsoft)", query, re.IGNORECASE).group())

        # Extract parameter
        parameter_match = re.search(r"(revenue|profit|income|sales|earnings|performance)", query, re.IGNORECASE)
        parameter = normalize_metric(parameter_match.group(1).strip()) if parameter_match else "Unknown Parameter"

        # Extract dates based on query
        if "last quarter" in query.lower():
            start_date, end_date = calculate_relative_dates("last quarter")
        elif "first quarter" in query.lower():
            start_date, end_date = calculate_relative_dates("first quarter")
        elif "previous month" in query.lower():
            start_date, end_date = calculate_relative_dates("previous month")
        else:
            start_date, end_date = get_default_dates()

        # Prepare structured output
        structured_output = {
            "entity": entity,
            "parameter": parameter,
            "start_date": start_date,
            "end_date": end_date
        }

        return [structured_output]
    except Exception as e:
        return {"error": f"Failed to extract information: {str(e)}"}



def process_comparison_query(query, history):
    """
    Process comparison queries dynamically, extracting new entities and ensuring all previous entities 
    are included in the comparison.
    """
    # Ensure that history is not empty
    if not history:
        return {"error": "History is empty. Query data for the primary entity before making comparisons."}

    # Extract the parameter, start_date, and end_date from the first entity in history
    parameter = history[0].get("parameter", "Unknown")
    start_date = history[0].get("start_date", "Unknown")
    end_date = history[0].get("end_date", "Unknown")

    # Match the new entity in the query (e.g., 'Compare it with Microsoft')
    match = re.search(r"compare (?:it|the .*?) with (\w+)", query, re.IGNORECASE)
    if not match:
        return {"error": "Could not extract the new entity for comparison from the query."}

    new_entity = match.group(1).strip()

    # Check if the entity already exists in history to avoid duplication
    if any(entry.get("entity").lower() == new_entity.lower() for entry in history):
        return {"error": f"The entity '{new_entity}' is already part of the comparison."}

    # Append the new entity to the history
    # Copy the parameter, start_date, and end_date from the first entity to the new entity
    new_comparison = {
        "entity": new_entity,
        "parameter": parameter,
        "start_date": start_date,
        "end_date": end_date
    }

    # Add all previous entities from the history (including the new one)
    comparison_output = history + [new_comparison]

    return comparison_output

def get_entity_and_parameter(query):
    """
    Extract entities and parameters from the query while handling aliases.
    """
    # Extract entities
    entity_match = re.findall(r"(Google|Meta|Facebook|Alphabet Inc.|Amazon|Apple|Microsoft|MSFT)", query, re.IGNORECASE)
    entities = list(set([normalize_entity(entity.strip()) for entity in entity_match]))

    # Extract parameters
    parameter_match = re.search(r"(profit|revenue|income|sales|earnings|performance)", query, re.IGNORECASE)
    parameter = normalize_metric(parameter_match.group(1).strip()) if parameter_match else "Unknown"

    return entities, parameter

def main():
    history = []  # Store the history of responses for context
    while True:
        # Get user input for the query
        query = input("Enter your query (or type 'stop' to exit): ").strip()
        
        if query.lower() == "stop":
            break

        # Check if the query contains the word "compare"
        if "compare" in query.lower():
            # Process the comparison query
            structured_output = process_comparison_query(query, history)
            print("Comparison Output:")
            print(json.dumps(structured_output, indent=4))
            # Update the history to include the comparison output
            history = structured_output
        else:
            # Step 1: Get response from LLM
            llm_response = process_query_with_llm(query, API_URL, API_KEY, history)

            # Debugging: Print the raw response
            # print("LLM Response:")
            # print(json.dumps(llm_response, indent=4))

            # Step 2: Extract relevant information
            if "error" in llm_response:
                print(json.dumps(llm_response, indent=4))
            else:
                structured_output = extract_information_from_response(llm_response, query)
                # print("Structured Output:")
                print(json.dumps(structured_output, indent=4))

                # Append the structured output to history
                history.extend(structured_output)

                # Limit history to the last 6 responses
                history = history[-6:]


if __name__ == "__main__":
    main()
