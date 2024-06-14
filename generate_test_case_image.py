import google.generativeai as genai
import configparser
from PIL import Image
import io

# Fetch keys from environment variables
config = configparser.ConfigParser()
config.read('test_case.env')

# Attempt to retrieve the API key from the configuration file
try:
    api_key = config.get('GEMINI', 'GOOGLE_API_KEY')
except Exception as e:
    print("Error reading API key from config:", e)
    api_key = None

# Check if the API key was successfully retrieved
if api_key:
    # Configure the generative AI model with the API key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
else:
    print("API key not found, model configuration skipped.")

# Function to generate test cases from image
def generate_test_cases_image(cleaned_prompt, image):
    try:
        # print("Entering generate_test_cases_image")
        # print(f"cleaned_prompt: {cleaned_prompt}")
        
        # Convert image to bytes
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        
        # print("Image converted to byte array")
        
        # Pass the image bytes to the generative AI model
        # print("Calling model.generate_content")
        model_response = model.generate_content([cleaned_prompt, Image.open(img_byte_array)], stream=True)
        
        # print("Resolving model_response")
        model_response.resolve()
        
        print("---"*15,"Model response:")
        print(model_response.text)  # Print the entire response for inspection
        # return model_response.text
        # # Attempt to extract text from model_response
        # result_text = ""
        if isinstance(model_response, list):
            for response in model_response:
                if hasattr(response, 'text'):
                    result_text += response.text
                else:
                    print("Response does not have a 'text' attribute:", response)
        elif hasattr(model_response, 'text'):
            result_text = model_response.text
        else:
            # print("Unexpected model_response format")
            result_text = str(model_response)
        
        return result_text

    except Exception as e:
        print(f"Error in generate_test_cases_image: {e}")
        return str(e)

# Function to modify and create a better prompt from the user query considering all the information being fetched
def modify_prompt(testCaseType, language, checkboxes, numberOfTestCases, image):
    # Convert checkboxes list to a comma-separated string
    checkboxes_str = ", ".join(checkboxes)

    clean_prompt = f"""
    Create {testCaseType} test cases in {language} for the given image. Cover all the widgets 
    seen on the image, in bullet points covering all these {numberOfTestCases} points.
    Strictly give {checkboxes_str} scenarios .
    """
    print(f"Generated prompt: {clean_prompt}")
    try:
        test_cases = generate_test_cases_image(clean_prompt, image)
        # print(test_cases)
        return test_cases
    except Exception as e:
        print(f"Error in modify_prompt: {e}")
        return str(e)