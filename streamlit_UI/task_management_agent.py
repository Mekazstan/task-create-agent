from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil import parser
import streamlit as st
import json
import os

from todoist_api_python.api import TodoistAPI

from langchain_core.tools import tool
from langchain_cohere import ChatCohere
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage

load_dotenv()

# Loading the model
cohere_api_token = os.getenv('COHERE_API_KEY', '')

# Initializing Todoist API
todoist_api_key = os.getenv('TODOIST_API_KEY', '')
todoist_api_instance = TodoistAPI(todoist_api_key)



# ~~~~~~~~~~~~~~~~~~~~~ AI Agent Tool Functions ~~~~~~~~~~~~~~~~~~~~~~~~

@tool
def get_user_projects():
    """
    Retrieves all projects for the given Todoist API token.
    
    Example call:

    get_user_projects()

    Args:
        api_token (str): The Todoist API token.

    Returns:
        list: A list of dictionaries, where each dictionary represents a project 
            and contains its ID, name, and other relevant attributes.
        str: An error message if the API call fails.
    """   
    try:
        all_projects = todoist_api_instance.get_projects()
        # Convert each Project object to a dictionary manually
        return [
            {
                "id": project.id,
                "name": project.name,
                "comment_count": project.comment_count,
                "order": project.order,
                "color": project.color,
                "is_shared": project.is_shared,
                "is_favorite": project.is_favorite,
                "is_inbox_project": project.is_inbox_project,
                "is_team_inbox": project.is_team_inbox,
                "view_style": project.view_style,
                "url": project.url,
                "parent_id": project.parent_id,
            }
            for project in all_projects
        ]
    except Exception as e:
        return f"Error retrieving projects: {e}"

@tool
def create_new_project(project_name: str):
  """
  Creates a project in Todoist given the name of the project.
  
  Example call:

    create_new_project("Test Project")

  Args:
      project_name (str): The name of the project to create in Todoist.

  Returns:
      str: The JSON response of the API call, including the ID of the created project, or an error message.
  """

  try:
    # Create a project using the Todoist API with the provided name
    new_project = todoist_api_instance.add_project(name=project_name)
    
    # Convert the Project object to a dictionary manually
    return {
        "id": new_project.id,
        "name": new_project.name,
        "comment_count": new_project.comment_count,
        "order": new_project.order,
        "color": new_project.color,
        "is_shared": new_project.is_shared,
        "is_favorite": new_project.is_favorite,
        "is_inbox_project": new_project.is_inbox_project,
        "is_team_inbox": new_project.is_team_inbox,
        "view_style": new_project.view_style,
        "url": new_project.url,
        "parent_id": new_project.parent_id,
    }
  except Exception as e:
      # Handle potential exceptions during API call
      return f"Error creating project: {e}"

@tool
def get_project(project_name: str):
    """
    Creates a project in Todoist given the name of the project.

    Example call:

    get_project("Test Project")

    Args:
        project_name (str): The name of the project in Todoist.

    Returns:
        str: The JSON response of the API call, including the ID of the project, or an error message.
    """
    try:
        all_projects = todoist_api_instance.get_projects()
        project_id = next((project.id for project in all_projects if project.name == project_name), '')
        if not project_id:
            return f"Project '{project_name}' not found."
        project = todoist_api_instance.get_project(project_id=project_id)
        return {
            "id": project.id,
            "name": project.name,
            "comment_count": project.comment_count,
            "order": project.order,
            "color": project.color,
            "is_shared": project.is_shared,
            "is_favorite": project.is_favorite,
            "is_inbox_project": project.is_inbox_project,
            "is_team_inbox": project.is_team_inbox,
            "view_style": project.view_style,
            "url": project.url,
            "parent_id": project.parent_id,
        }
    except Exception as e:
        return f"Error retrieving project: {e}"

@tool
def update_project(project_name: str, name: str):
    """
    Update/changes the name of a project in Todoist given the name of the project.

    Example call:

    update_project("Test Project", "New Project name")

    Args:
        project_name (str): The name of the project in Todoist.
        name (str): The new name of the project in Todoist.

    Returns:
        str: The JSON response of the API call, including the ID of the project, or an error message.
    """

    try:
        # Get all projects
        all_projects = todoist_api_instance.get_projects()

        # Find the project ID by name
        project_id = ''
        for project in all_projects:
            if project.name == project_name:
                project_id = project.id
                break

        if project_id == '':
            return f"Project '{project_name}' not found."
        # Update a project using the Todoist API with the provided name
        project = todoist_api_instance.update_project(project_id=project_id, name=name)
        return True, f"Project '{project_name}' updated successfully."
    except Exception as e:
        return False, f"Sorry I encoutered some errors while updating the project: {e}"

@tool
def delete_project(project_name: str):
    """
    Deletes a project in Todoist.

    Example call:

    delete_project(project_name="2995104339")

    Args:
        project_name (str): The name of the project to delete.

    Returns:
        bool: True if the project was deleted successfully, False otherwise.
        str: An error message if the API call fails.
    """

    try:
        all_projects = todoist_api_instance.get_projects()
        project_id = next((project.id for project in all_projects if project.name == project_name), '')
        if not project_id:
            return False, f"Project '{project_name}' not found."
        todoist_api_instance.delete_project(project_id)
        return True, f"Project '{project_name}' deleted successfully."
    except Exception as e:
        return False, f"Error deleting project: {e}"

@tool
def get_active_tasks(project_name: str):
  """
  Retrieves all active tasks within a specified project in Todoist by its name.
  
  Example
  get_active_tasks("project_name")
  
  Args:
      project_name (str): The name of the project to get active tasks from.

  Returns:
      list: A list of dictionaries representing the active tasks in the project,
          or an empty list if no tasks are found or the project is not found.
      str: An error message if the API call fails.
  """

  try:
      # Get all projects
      all_projects = todoist_api_instance.get_projects()

      # Find the project ID by name
      project_id = ''
      for project in all_projects:
          if project.name == project_name:
              project_id = project.id
              break

      if project_id == '':
          return [], f"Project '{project_name}' not found."

      # Get all active tasks in the project
      active_tasks = todoist_api_instance.get_tasks()

      # Convert tasks to dictionaries & get only active tasks
      return [task.to_dict() for task in active_tasks if task.project_id == project_id and not task.is_completed]

  except Exception as e:
      return [], f"Error getting active tasks: {e}"

@tool
def get_tasks_by_due_date(due_date: str):
    """
    Retrieves tasks from Todoist based on a specified due date filter.

    Example:
        get_tasks_by_due_date("today")

    Args:
        due_date (str): The due date filter to use, such as "today", "tomorrow", or a specific date.
        

    Returns:
        list: A list of dictionaries representing tasks that match the due date filter.
        str: An error message if the API call fails or no tasks are found.
    """
    today = f"The current date is: {datetime.now().date()}"
    try:
        # Get all tasks
        all_tasks = todoist_api_instance.get_tasks()
        
        if due_date == "today":
            due_date_str = today
            due_date_split = parser.parse(due_date_str.split(": ")[1])
            due_date = due_date_split.strftime("%Y-%m-%d")

        # Filter tasks by the specified due date
        filtered_tasks = [
            task.to_dict() for task in all_tasks 
            if task.due and task.due.date == due_date
        ]

        if not filtered_tasks:
            return [], f"No tasks found for the due date '{due_date}'."

        return filtered_tasks, None  # Return the filtered tasks and no error message

    except Exception as e:
        return [], f"Error retrieving tasks by due date: {e}"

@tool
def create_new_task(project_name: str, task_content: str, due_string: str):
    """
    Adds a new task to the specified project in Todoist by name.

    Example call:
        create_new_task("Test Project", "Create Chatbot", due_string="tomorrow at 12:00", priority=4)

    Args:
        project_name (str): The name of the project to add the task to.
        task_content (str): The content of the task (required).
        due_string (str, optional): A natural language string for the task's due date (e.g., "tomorrow at 12:00").

    Returns:
        dict: The details of the created task, or an error message if the operation fails.
    """
    try:
        all_projects = todoist_api_instance.get_projects()
        project_id = next((project.id for project in all_projects if project.name == project_name), '')
        if not project_id:
            return {"error": f"Project '{project_name}' not found."}
        new_task = todoist_api_instance.add_task(
            content=task_content,
            project_id=project_id,
            due_string=due_string
        )
        return {
            "id": new_task.id,
            "content": new_task.content,
            "description": new_task.description,
            "is_completed": new_task.is_completed,
            "due": new_task.due.to_dict() if new_task.due else '',
            "priority": new_task.priority,
            "project_id": new_task.project_id,
            "url": new_task.url,
        }
    except Exception as e:
        return {"error": f"Error adding task: {e}"}
  
@tool
def update_task(project_name: str, task_content: str, due_string: str):
    """
    Updates an existing task in Todoist by finding it based on project name and task content.
    
    Example call:
        update_task("Test Project", "Buy Milk", new_content="Buy Coffee", due_string="tomorrow")

    Args:
        project_name (str): The name of the project containing the task.
        task_content (str): The current content of the task to update.
        due_string (str, optional): The new due date string for the task (e.g., "tomorrow", "next week"). Defaults to an empty string.

    Returns:
        dict: The updated task details or an error message if the operation fails.
    """
    try:
        # Get all projects
        all_projects = todoist_api_instance.get_projects()

        # Find the project ID by name
        project_id = ''
        for project in all_projects:
            if project.name == project_name:
                project_id = project.id
                break

        if project_id == '':
            return {"error": f"Project '{project_name}' not found."}

        # Get all tasks in the project
        all_tasks = todoist_api_instance.get_tasks(project_id=project_id)

        # Find the task by content
        task_to_update = ''
        for task in all_tasks:
            if task.content == task_content:
                task_to_update = task
                break

        if task_to_update == '':
            return {"error": f"Task '{task_content}' not found in project '{project_name}'."}

        # Create a dictionary to hold the updated task data
        update_data = {}
        if due_string:
            update_data["due_string"] = due_string

        # Update the task using the Todoist API
        updated_task = todoist_api_instance.update_task(task_to_update.id, **update_data)

        return True, f"Task '{task_content}' updated successfully."
    except Exception as e:
        return False, f"Sorry I encoutered some errors while updating the tsak: {e}"
  
@tool
def complete_task(project_name: str, task_content: str):
    """
    Completes an existing task in Todoist by finding it based on project name and task content.
    
    Example call:
        complete_task("Test Project", "Buy Milk")

    Args:
        project_name (str): The name of the project containing the task.
        task_content (str): The current content of the task to complete.

    Returns:
        dict: A response indicating the status of the operation and task details if successful,
              or an error message if the operation fails.
    """
    try:
        # Get all projects
        all_projects = todoist_api_instance.get_projects()

        # Find the project ID by name
        project_id = ''
        for project in all_projects:
            if project.name == project_name:
                project_id = project.id
                break

        if project_id == '':
            return {"error": f"Project '{project_name}' not found."}

        # Get all tasks in the project
        all_tasks = todoist_api_instance.get_tasks(project_id=project_id)

        # Find the task by content
        task_to_complete = ''
        for task in all_tasks:
            if task.content == task_content:
                task_to_complete = task
                break

        if task_to_complete == '':
            return {"error": f"Task '{task_content}' not found in project '{project_name}'."}

        # Complete the task using the Todoist API
        todoist_api_instance.close_task(task_to_complete.id)

        # Return a success response with task details
        return {
            "status": "success",
            "message": f"Task '{task_content}' has been marked as complete.",
            "task_id": task_to_complete.id,
            "content": task_to_complete.content,
            "project_id": task_to_complete.project_id,
            "completed_at": task_to_complete.completed_at if hasattr(task_to_complete, 'completed_at') else '',
        }

    except Exception as e:
        return {"error": f"Error completing task: {e}"}



# Maps the function names to the actual function object in the script
# This mapping will also be used to create the list of tools to bind to the agent
available_functions = {
    "get_user_projects": get_user_projects,
    "create_new_project": create_new_project,
    "get_project": get_project,
    "update_project": update_project,
    "delete_project": delete_project,
    "get_active_tasks": get_active_tasks,
    "get_tasks_by_due_date": get_tasks_by_due_date,
    "create_new_task": create_new_task,
    "update_task": update_task,
    "complete_task": complete_task
}     


# ~~~~~~~~~~~~~~~~~~~~~~ AI Prompting Function ~~~~~~~~~~~~~~~~~~~~~~~~~

def prompt_ai(messages, nested_calls=0):
    if nested_calls > 5:
        raise "AI is tool calling too much!"

    # First, prompt the AI with the latest user message
    tools = [tool for _, tool in available_functions.items()]
    todoist_chatbot = ChatCohere(model="command-r-plus")
    todoist_chatbot_with_tools = todoist_chatbot.bind_tools(tools)

    stream = todoist_chatbot_with_tools.stream(messages)
    first = True
    for chunk in stream:
        if first:
            gathered = chunk
            first = False
        else:
            gathered = gathered + chunk

        yield chunk

    has_tool_calls = len(gathered.tool_calls) > 0

    # Second, see if the AI decided it needs to invoke a tool
    if has_tool_calls:
        # Add the tool request to the list of messages so the AI knows later it invoked the tool
        messages.append(gathered)

        # If the AI decided to invoke a tool, invoke it
        # For each tool the AI wanted to call, call it and add the tool result to the list of messages
        for tool_call in gathered.tool_calls:
            tool_name = tool_call["name"].lower()
            selected_tool = available_functions[tool_name]
            tool_output = selected_tool.invoke(tool_call["args"])
            messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))                

        # Call the AI again so it can produce a response with the result of calling the tool(s)
        additional_stream = prompt_ai(messages, nested_calls + 1)
        for additional_chunk in additional_stream:
            yield additional_chunk


# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~

system_message = f"""
You are a personal assistant who helps manage tasks in Todoist. 
You never give IDs to the user since those are just for you to keep track of.
When a user asks to create a task and you don't know the project to add it to for sure, clarify with the user.
The current date is: {datetime.now().date()}
"""

def main():
    st.title("Todoist Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=system_message)
        ]    

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        message_json = json.loads(message.model_dump_json())
        message_type = message_json["type"]
        if message_type in ["human", "ai", "system"]:
            with st.chat_message(message_type):
                st.markdown(message_json["content"])        

    # React to user input
    if prompt := st.chat_input("What would you like to do today?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            stream = prompt_ai(st.session_state.messages)
            response = st.write_stream(stream)
        
        st.session_state.messages.append(AIMessage(content=response))


if __name__ == "__main__":
    main()