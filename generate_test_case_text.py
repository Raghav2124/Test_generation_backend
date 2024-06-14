import requests
import json
import openai
import configparser

# fetch keys from environment variables
config = configparser.ConfigParser()
config.read('test_case.env')
API_KEY = config.get('OPENAI', 'API_KEY')
API_URL = config.get('OPENAI', 'API_URL')

# fetch the openai keys
openai.api_key = API_KEY

# function to generate test cases from text
def generate_test_cases(clean_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": clean_prompt}
            ],
            max_tokens=1500,
            temperature=0.9
        )
        
        # Print out the response content before parsing it
        print("Response content:", response['choices'][0]['message']['content'])
        
        # Manually structure the response content in JSON format
        
        
        return response['choices'][0]['message']['content']  # Return as JSON
    except Exception as e:
        return str(e)

# function to modify and create a better prompt from the user query considering all the information being fetched
def modify_prompt(testCaseType, language, scenario, checkboxes, numberOfTestCases):
    clean_prompt = f"""Create {testCaseType} test cases in {language} for the {scenario}
in bullet points covering all these points: {', '.join(checkboxes)}.
Strictly give {numberOfTestCases} cases , give the result in json format """
    try:
        test_cases = generate_test_cases(clean_prompt)
        return test_cases
    except Exception as e:
        return str(e)
