from dotenv import load_dotenv
import os

from todoist_api_python.api import TodoistAPI

load_dotenv()

# Initialize Todoist API
todoist_api_key = os.getenv('TODOIST_API_KEY', '')
todoist_api_instance = TodoistAPI(todoist_api_key)

# ~~~~~~~~~~~~~~~~~~~~~ AI Agent Tool Functions ~~~~~~~~~~~~~~~~~~~~~~~~


def get_user_projects():
    try:
        all_projects = todoist_api_instance.get_projects()
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


def create_new_project(project_name):
    try:
        new_project = todoist_api_instance.add_project(name=project_name)
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
        return f"Error creating project: {e}"


def get_project(project_name):
    try:
        all_projects = todoist_api_instance.get_projects()
        project_id = next((project.id for project in all_projects if project.name == project_name), None)
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


def delete_project(project_name):
    try:
        all_projects = todoist_api_instance.get_projects()
        project_id = next((project.id for project in all_projects if project.name == project_name), None)
        if not project_id:
            return False, f"Project '{project_name}' not found."
        todoist_api_instance.delete_project(project_id)
        return True, f"Project '{project_name}' deleted successfully."
    except Exception as e:
        return False, f"Error deleting project: {e}"


def create_new_task(project_name, task_content, due_string=None, due_lang="en", priority=1):
    try:
        all_projects = todoist_api_instance.get_projects()
        project_id = next((project.id for project in all_projects if project.name == project_name), None)
        if not project_id:
            return {"error": f"Project '{project_name}' not found."}
        new_task = todoist_api_instance.add_task(
            content=task_content,
            project_id=project_id,
            due_string=due_string,
            due_lang=due_lang,
            priority=priority,
        )
        return {
            "id": new_task.id,
            "content": new_task.content,
            "description": new_task.description,
            "is_completed": new_task.is_completed,
            "due": new_task.due.to_dict() if new_task.due else None,
            "priority": new_task.priority,
            "project_id": new_task.project_id,
            "url": new_task.url,
        }
    except Exception as e:
        return {"error": f"Error adding task: {e}"}

def get_active_tasks(project_name):
    """
    Retrieves all active tasks within a specified project in Todoist by its name.

    Args:
        project_name (str): The name of the project to get active tasks from.

    Returns:
        list: A list of dictionaries representing the active tasks in the project,
            or an empty list if no tasks are found or the project is not found.
        str: An error message if the API call fails.
    """
    try:
        all_projects = todoist_api_instance.get_projects()

        project_id = None
        for project in all_projects:
            if project.name == project_name:
                project_id = project.id
                break

        if project_id is None:
            return [], f"Project '{project_name}' not found."

        active_tasks = todoist_api_instance.get_tasks()
        return [task.to_dict() for task in active_tasks if task.project_id == project_id and not task.is_completed]

    except Exception as e:
        return [], f"Error getting active tasks: {e}"

def update_task(project_name, task_content, new_content=None, due_string=None):
    """
    Updates an existing task in Todoist by finding it based on project name and task content.

    Args:
        project_name (str): The name of the project containing the task.
        task_content (str): The current content of the task to update.
        new_content (str, optional): The new content for the task. Defaults to None.
        due_string (str, optional): The new due date string for the task (e.g., "tomorrow"). Defaults to None.

    Returns:
        dict: The updated task details or an error message if the operation fails.
    """
    try:
        all_projects = todoist_api_instance.get_projects()

        project_id = None
        for project in all_projects:
            if project.name == project_name:
                project_id = project.id
                break

        if project_id is None:
            return {"error": f"Project '{project_name}' not found."}

        all_tasks = todoist_api_instance.get_tasks(project_id=project_id)

        task_to_update = None
        for task in all_tasks:
            if task.content == task_content:
                task_to_update = task
                break

        if task_to_update is None:
            return {"error": f"Task '{task_content}' not found in project '{project_name}'."}

        update_data = {}
        if new_content:
            update_data["content"] = new_content
        if due_string:
            update_data["due_string"] = due_string

        updated_task = todoist_api_instance.update_task(task_to_update.id, **update_data)
        return {
            "id": updated_task.id,
            "content": updated_task.content,
            "due": updated_task.due.to_dict() if updated_task.due else None,
            "priority": updated_task.priority,
            "project_id": updated_task.project_id,
            "url": updated_task.url,
            "created_at": updated_task.created_at,
            "labels": updated_task.labels,
        }

    except Exception as e:
        return {"error": f"Error updating task: {e}"}

def complete_task(project_name, task_content):
    """
    Completes an existing task in Todoist by finding it based on project name and task content.

    Args:
        project_name (str): The name of the project containing the task.
        task_content (str): The current content of the task to complete.

    Returns:
        dict: A response indicating the status of the operation and task details if successful,
              or an error message if the operation fails.
    """
    try:
        all_projects = todoist_api_instance.get_projects()

        project_id = None
        for project in all_projects:
            if project.name == project_name:
                project_id = project.id
                break

        if project_id is None:
            return {"error": f"Project '{project_name}' not found."}

        all_tasks = todoist_api_instance.get_tasks(project_id=project_id)

        task_to_complete = None
        for task in all_tasks:
            if task.content == task_content:
                task_to_complete = task
                break

        if task_to_complete is None:
            return {"error": f"Task '{task_content}' not found in project '{project_name}'."}

        todoist_api_instance.close_task(task_to_complete.id)
        return {
            "status": "success",
            "message": f"Task '{task_content}' has been marked as complete.",
            "task_id": task_to_complete.id,
            "content": task_to_complete.content,
            "project_id": task_to_complete.project_id,
        }

    except Exception as e:
        return {"error": f"Error completing task: {e}"}



# ~~~~~~~~~~~~~~~~~~~~~ Testing Functions ~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    # # Test creating a new project
    # print("\nCreating a new project:")
    # print(create_new_project("Test Project"))
    
    # # Test getting user projects
    # print("Fetching all projects:")
    # print(get_user_projects())

    # # Test deleting a project
    # print("\nDeleting a project:")
    # print(delete_project("Test Project"))
    
    # # Test fetching a specific project
    # print("\nFetching a specific project:")
    # print(get_project("Test Project"))

    # # Test creating a new task
    # print("\nCreating a new task in 'Test Project':")
    # print(create_new_task("Test Project", "Complete the Python script", due_string="tomorrow"))

    # # Test update_task
    # print("Updating Task")
    # print(update_task("Test Project", "Complete the Python script", new_content="Updated Python Script", due_string="tomorrow"))
    
    # Test get_active_tasks
    print("Getting active Task")
    print(get_active_tasks("Test Project"))

    # # Test complete_task
    # print("Completing Task")
    # print(complete_task("Test Project", "Updated Python Script"))

