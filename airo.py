import requests
import json
import os
import sys
import traceback
import ollama

url = "http://localhost:11343/api/generate"

def generate_answers(agent, prompt):
    if agent == 'projektplaner':
        model_name = 'stablelm2:1.6b-zephyr-fp16'
    elif agent == 'coder':
        model_name = 'codellama:7b'
    else:
        raise ValueError("Unknown Agent.")

    # Create a message with the user's role and the passed prompt.
    messages = [
        {
            'role': 'user',
            'content': prompt,
        },
    ]

    # Send the message to the model and get the response.
    try:
        response = ollama.chat(model=model_name, messages=messages)
        return response['message']['content']
    except Exception as e:
        print(f"There was an error communicating with the Ollama model: {e}")
        return None


# ancient:
# def generate_answers(agent, prompt):
    header_project_planner = {
        "Content-Type": "application/json"
    }

    data_project_planner = {
        "model": "stablelm2:1.6b-zephyr-fp16",
        "prompt": prompt,
        "stream": False
    }

    header_coder = {
        "Content-Type": "application/json"
    }

    data_coder = {
        "model": "codellama:7b",
        "prompt": prompt,
        "stream": False
    }

    if agent == 'project_planner':
        headers = header_project_planner
        data = data_project_planner
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response
    
    if agent == 'coder':
        headers = header_coder
        data = data_coder
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response

def service_desk(input):
    response = generate_answers("project_planner", f"Pose meaningful questions for the following project, enabling a very detailed project plan to be created: {input}")
    return response

def service_desk2(answered_questions):

    complete_project = generate_answers(f"Create a ")

def project_planner(proj):
    project = f"Create a detailed project plan for the following project: {proj}"
    response = generate_answers("project_planner", project)
    manager(response)
    
def manager(project_plan):
    """
    manager takes project_plan, generates request to divide tasks for coder instances, which then generate code snippets and then calls coder instances based on number of tasks (response is split into tasks (markdown format), tasks = list, )
    """
    prompt = f"Divide the following project into individual tasks. Once the task listing begins, signal this with a --- . Task listings should be in Markdown. Here's the project plan: {project_plan}"
    tasks_response = generate_answers("project_planner", prompt)
    tasks = tasks_response['text'].split('---')[1].strip().split('\n')  # Assumption that the task list comes after '---'
    # Call a coder instance for each task (here exemplified)
    for task in tasks:
        coder_instance(task)

def generate_file_structure(task_list):
    """
    Creates folders and files based on a list of tasks.
    This function is a placeholder and needs to be implemented according to project requirements.
    """
    # Example structure: One folder per task
    for task in task_list:
        folder_name = task.replace(" ", "_").lower()  # Replace spaces with underscores and lowercase
        os.makedirs(folder_name, exist_ok=True)  # Create folder if not exists
        # Here you could add an initial file or a README
        with open(f"{folder_name}/README.md", 'w') as f:
            f.write(f"Project: {task}\n")

def coder_instance(task):
    """
    Generates code based on a specific task, removes the first word, and writes the code to a file.
    """
    code_response = generate_answers("coder", task)
    code_text = code_response['text']
    language, *code = code_text.split('```', 1)  # Separate programming language from code
    code = ''.join(code)  # Rejoin the code without the programming language
    
    # Create filename based on the task
    filename = task.replace(" ", "_").lower() + ".txt"  # Example: use .txt as file extension, customizable
    
    with open(filename, 'w') as file:
        file.write(code)
    
    return code

def testing(code, test_cases):
    """
    Tests the generated code using a debugger. Automatically corrects the code if errors occur and repeats the process
    until the code can be successfully executed.
    
    :param code: The code to be tested as a string.
    :return: A tuple with the status of the code (True for success, False for failure) and the tested or corrected code.
    """
    corrected_code = code
    success = False

    while not success:
        temp_stdout = sys.stdout  # Temporarily store the standard output
        sys.stdout = open('debug_log.txt', 'w')  # Redirect output to a file
        try:
            exec(corrected_code)  # Attempt to execute the code
            sys.stdout.close()
            sys.stdout = temp_stdout  # Restore the original standard output
            success = True  # No errors, test successful
        except Exception as e:
            sys.stdout.close()
            sys.stdout = temp_stdout  # Restore the original standard output
            error_message = ''.join(traceback.format_exception(None, e, e.__traceback__))  # Error message
            corrected_code = correction(corrected_code + "\n# Error: " + error_message)  # Attempt to correct the code

    return (True, corrected_code)  # Return the corrected code


def correction(code):
    correction_prompt = f"Please correct the following code: {code}"
    correction_response = generate_answers("coder", correction_prompt)
    return correction_response.json()['text']

def documentation(code):
    documentation_prompt = f"Create documentation for the following code in the form of a Github ReadMe: {code}"
    documentation_response = generate_answers("coder", documentation_prompt)
    return documentation_response.json()['text']


if __name__ == '__main__':
  project_description = input("Please provide detailed input for your project: ")
  service_desk(project_description)
  specified_project_description = input("Answers to questions: ")
  service_desk2()
  complete_project = f"Create detailed steps and a complete guide for the following project: "


