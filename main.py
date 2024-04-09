import requests
import json
import os
import sys
import traceback
import ollama
import dotenv
import subprocess

dotenv.load_dotenv()  # Load environment variables
PROJECT_PLANNER_MODEL = os.getenv("PROJECT_PLANNER_MODEL", "stablelm2:1.6b-zephyr-fp16")
CODER_MODEL = os.getenv("CODER_MODEL", "codellama:7b")

def generate_answers(agent, prompt):
    model_name = ""
    if agent == 'project_planner':
        model_name = PROJECT_PLANNER_MODEL
    elif agent == 'coder':
        model_name = CODER_MODEL
    if not model_name:
        raise ValueError("Model name is not specified in the environment variables or defaults are missing.")
    messages = [
        {
            'role': 'user',
            'content': prompt,
        },
    ]
    try:
        response = ollama.chat(model=model_name, messages=messages)
        return response['message']['content']
    except Exception as e:
        print(f"There was an error communicating with the Ollama model: {e}")
        return None

def service_desk(input):
    response = generate_answers("project_planner", f"Pose meaningful questions for the following project, enabling a very detailed project plan to be created: {input}")
    return response

def service_desk2(answered_questions):
    complete_project = generate_answers("project_planner", f"Create a detailed project plan for the following: {answered_questions}")
    return complete_project

def project_planner(proj):
    project = f"Create a detailed project plan for the following project: {proj}"
    response = generate_answers("project_planner", project)
    return manager(response)
   
def manager(project_plan):
    """
    manager takes project_plan, generates request to divide tasks for coder instances, which then generate code snippets and then calls coder instances based on number of tasks (response is split into tasks (markdown format), tasks = list, )
    """
    prompt = f"Divide the following project into individual tasks. Once the task listing begins, signal this with a --- . Task listings should be in Markdown. Here's the project plan: {project_plan}"
    tasks_response = generate_answers("project_planner", prompt)
    tasks = tasks_response.split('---')[1].strip().split('\n')  # Assumption that the task list comes after '---'
   
    # Generate file structure based on tasks
    generate_file_structure(tasks)
   
    # Call a coder instance for each task
    code_snippets = []
    for task in tasks:
        code_snippet = coder_instance(task)
        code_snippets.append(code_snippet)
   
    # Test    
    tested_code_snippets = []
    for code_snippet in code_snippets:
        success, tested_code = testing(code_snippet, [])  # Provide test cases if needed
        tested_code_snippets.append(tested_code)
   
    # Generate documentation
    documentation(tested_code_snippets)
   
    # Install dependencies
    install_dependencies()

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
    code_text = code_response
    language, *code = code_text.split('```', 1)  # Separate programming language from code
    code = ''.join(code)  # Rejoin the code without the programming language
   
    # Create filename based on the function of the code
    filename = task.replace(" ", "_").lower() + "_function.txt"  # Example: use .txt as file extension, customizable
   
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
    return correction_response

def documentation(code_snippets):
    """
    Create documentation for the code snippets in the form of a Github ReadMe.
    """
    documentation_prompt = f"Create documentation for the following code snippets in the form of a Github ReadMe: {code_snippets}"
    documentation_response = generate_answers("coder", documentation_prompt)
   
    project_structure = "## Project Structure\n"
    for code_snippet in code_snippets:
        task = code_snippet.split('\n')[0].strip()  # Assuming the first line of each code snippet is the task description
        folder_name = task.replace(" ", "_").lower()
        project_structure += f"- {folder_name}/\n    - {task.replace(' ', '_').lower()}_function.py\n"
   
    documentation_content = f"# Project Documentation\n\n{project_structure}\n{documentation_response}"
   
    with open('README.md', 'w') as file:
        file.write(documentation_content)


def install_dependencies():
    """
    Install project dependencies automatically based on file extensions or generated code outputs.
    """
    print("Installing project dependencies...")
    
    # Detect programming language based on file extensions
    file_extensions = set()
    for root, dirs, files in os.walk("."):
        for file in files:
            _, extension = os.path.splitext(file)
            file_extensions.add(extension)
    
    # Install dependencies based on programming language
    if ".py" in file_extensions:
        # Python dependencies
        print("Installing Python dependencies...")
        
        # Check if requirements.txt exists
        if os.path.exists("requirements.txt"):
            subprocess.run(["pip", "install", "-r", "requirements.txt"])
        else:
            # Try to install common Python packages
            common_packages = ["requests", "numpy", "pandas", "matplotlib"]
            for package in common_packages:
                try:
                    subprocess.run(["pip", "install", package])
                except subprocess.CalledProcessError:
                    print(f"Failed to install package: {package}")
    
    if ".js" in file_extensions:
        # JavaScript dependencies
        print("Installing JavaScript dependencies...")
        
        # Check if package.json exists
        if os.path.exists("package.json"):
            subprocess.run(["npm", "install"])
        else:
            # Try to install common JavaScript packages
            common_packages = ["axios", "lodash", "moment"]
            for package in common_packages:
                try:
                    subprocess.run(["npm", "install", package])
                except subprocess.CalledProcessError:
                    print(f"Failed to install package: {package}")
    
    # Analyze generated code outputs for additional dependencies
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".txt"):  # Assuming generated code is stored in .txt files
                with open(os.path.join(root, file), "r") as f:
                    code = f.read()
                    
                    # Python dependencies
                    if "import" in code:
                        lines = code.split("\n")
                        for line in lines:
                            if line.startswith("import") or line.startswith("from"):                                
                                package = line.split()[1].split(".")[0]
                                try:
                                    subprocess.run(["pip", "install", package])
                                except subprocess.CalledProcessError:
                                    print(f"Failed to install package: {package}")
                    
                    # JavaScript dependencies
                    if "require" in code:
                        lines = code.split("\n")
                        for line in lines:
                            if line.startswith("const") or line.startswith("var"):
                                package = line.split("=")[1].split("(")[1].split(")")[0].strip("'\"")
                                try:
                                    subprocess.run(["npm", "install", package])
                                except subprocess.CalledProcessError:
                                    print(f"Failed to install package: {package}")
    
    print("Dependency installation completed.")


if __name__ == '__main__':
    project_description = input("Please provide detailed input for your project: ")
    response = service_desk(project_description)
    print(response)
    specified_project_description = ""
    while True:
        new_specified_description = input("Please provide or update your answers to questions: ")
        specified_project_description += " " + new_specified_description  # Update with additional details
        response2 = service_desk2(specified_project_description)
        print(response2)
        agreement = input("Are you good with this? (y/n): ")
        if agreement.lower() == 'y':
            break
        else:
            print("Please provide further details.")
    complete_project = f"Create detailed steps and a complete guide for the following project: {project_description} ; {specified_project_description} ; {response2}"
    project_planner(complete_project)
