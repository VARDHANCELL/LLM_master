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



Installation

1. Navigate to the project directory:

	cd llm.py

2. Install dependencies:

	pip install requests
	pip install python-dateutil

Steps to Generate an API Key for the Groq LLM API

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


Usage

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

Configuration

1. Aliases

	Modify the entity_aliases and metric_aliases dictionaries in the code to add new aliases for entities and metrics.
	Aliases can be more than what are defined

2. Default Dates

	Update the get_default_dates function to change the default date ranges when no dates are specified.


Evaluation Criteria

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


Testing

Run the application and input the following test queries to validate functionality:

	"What is the profit of Apple in the last month?"

	"Compare Microsoft's revenue with Google's profit this quarter."

	"How much did Amazon earn last year?"

Verify the JSON output for accuracy and completeness.

Area's to improve:

Due to shortage of time I am not able to deliver the best and efficient application on llm but for your reference i can list down the current area's to improve in my code which can be fixed by me if given some proper time and discussion.

1. Duplicacy in history
2. Entity's name mismatch in query
3. Can integrate more ambiguous time frames like 1st quarter or any specific month like January
4. The process of extraction of entity and parameters from the query can be modified for different types of query structure ; currently working for 1 structure only
5. I think it is a type of project which can be greatly enhanced everytime you look into it