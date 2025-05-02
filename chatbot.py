import os
import uuid  # Import the uuid module to generate unique session IDs
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

# path for api key 
credentials_path = 'C:/Users/Vinay Singh Baghel/OneDrive/Desktop/AI_Health_Tracker/credentials/your-service-account-file.json'  # Path to the service account key

# Initialize the Dialogflow client
credentials = service_account.Credentials.from_service_account_file(credentials_path)
client = dialogflow.SessionsClient(credentials=credentials)

def talk_to_bot(text, session_id=None, project_id='healthbot-ueco'):
    """ Function to interact with Dialogflow and get the bot response """
    try:
        # Create a unique session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())  # Generate a random session ID
        
        session = client.session_path(project_id, session_id)
        
        text_input = dialogflow.types.TextInput(text=text, language_code='en')
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = client.detect_intent(session=session, query_input=query_input)
        
        # Print the response for debugging
        print(f"Bot Response: {response.query_result.fulfillment_text}")
        return response.query_result.fulfillment_text  # Return the response text (response from Dialogflow)
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred while talking to the bot."

# Example interaction with the bot
response = talk_to_bot("Hello, how are you?")
print(response)  # Optionally, print the response for testing
