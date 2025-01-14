import cohere
import asana
from asana.rest import ApiException
from dotenv import load_dotenv
from datetime import datetime
import json
import os

load_dotenv()

api_token = os.getenv('COHERE_API_KEY')
client = cohere.Client(api_token)


configuration = asana.Configuration()
configuration.access_token = os.getenv('ASANA_ACCESS_TOKEN', '')
api_client = asana.ApiClient(configuration)

tasks_api_instance = asana.TasksApi(api_client)

def create_asana_task(task_name, due_on="today"):
    """
    Creates a task in Asana given the name of the task and when it is due

    Example call:

    create_asana_task("Test Task", "2024-06-24")
    Args:
        task_name (str): The name of the task in Asana
        due_on (str): The date the task is due in the format YYYY-MM-DD. If not given, the current day is used
    Returns:
        str: The API response of adding the task to Asana or an error message if the API call threw an error
    """
    if due_on == "today":
        due_on = str(datetime.now().date())

    task_body = {
        "data": {
            "name": task_name,
            "due_on": due_on,
            "projects": [os.getenv("ASANA_PROJECT_ID", "")]
        }
    }

    try:
        api_response = tasks_api_instance.create_task(task_body, {})
        return json.dumps(api_response, indent=2)
    except ApiException as e:
        return f"Exception when calling TasksApi->create_task: {e}"

def get_tools():
    tools = [
        {
            "name": "create_asana_task",
            "description": "Creates a task in Asana given the name of the task and when it is due",
            "parameter_definitions": {
                "task_name": {
                    "description": "The name of the task in Asana",
                    "type": "str",
                    "required": True,
                },
                "due_on": {
                    "description": "The date the task is due in the format YYYY-MM-DD. If not given, the current day is used",
                    "type": "str",
                    "required": False,
                }
            },
        }
    ]

    return tools


def prompt_ai(messages):
    """
    Function to send a chat request to Cohere and return the generated response
    Args:
        messages (list): List of dictionaries containing role and message content
    Returns:
        str: The generated response from Cohere
    """
    chat_history = [
        {
            "role": "System",
            "message": f"You are a personal assistant who helps manage tasks in Asana. The current date is: {datetime.now().date()}"
        }
    ]
    for message in messages:
        if message.get("role") not in ["user", "assistant"]:
            continue
        role_mapping = {
            "user": "User",
            "assistant": "Chatbot",
            "tool": "Tool"
        }
        chat_history.append({
            "role": role_mapping.get(message.get("role")),
            "message": message.get("content")
        })

    model = 'command-r-08-2024'
    temperature = 0.3
    try:
        response = client.chat(
            model=model,
            message=messages[-1].get("content"),
            temperature=temperature,
            chat_history=chat_history,
            prompt_truncation='AUTO',
            tools=get_tools()
        )

        response_message = response.text
        if hasattr(response, 'tools') or hasattr(response, 'tool_calls'):
            tool_calls = getattr(response, 'tools', getattr(response, 'tool_calls', None))
            if tool_calls:
                available_functions = {
                    "create_asana_task": create_asana_task
                }
                messages.append(response_message)
                for tool_call in tool_calls:
                    function_name = tool_call.name
                    function_to_call = available_functions[function_name]
                    function_args = tool_call.parameters
                    function_response = function_to_call(**function_args)
                    messages.append({
                        "role": "tool",
                        "name": function_name,
                        "content": function_response
                    })
                second_response = client.chat(
                    model=model,
                    message=messages[-1].get("content"),
                    temperature=temperature,
                    chat_history=chat_history
                )
                return second_response.text
        return response.text
    except Exception as e:
        print(f"Cohere API Error: {e}")
        return None 

def main():
  messages = [
      {
          "role": "system",
          "content": f"You are a personal assistant who helps manage tasks in Asana. The current date is: {datetime.now().date()}"
      }
  ]

  while True:
      user_input = input("Chat with AI (q to quit): ").strip()

      if user_input == 'q':
          break

      messages.append({"role": "user", "content": user_input})
      ai_response = prompt_ai(messages)

      if ai_response:
        print(ai_response)
      else:
        print("An error occurred while processing your request.")

      messages.append({"role": "assistant", "content": ai_response})


if __name__ == "__main__":
  main()
  