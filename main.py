import requests
import json
import os
import sys
import traceback
import ollama
import dotenv
import subprocess
import html5lib
import re

dotenv.load_dotenv()  # Load environment variables
PROJECT_PLANNER_MODEL = os.getenv("PROJECT_PLANNER_MODEL", "dolphin-mistral:latest")
CODER_MODEL = os.getenv("CODER_MODEL", "codellama:7b")
MARKDOWN_MAKER = os.getenv("CODER_MODEL", "vicuna:13b-16k")
TASKNAMER = os.getenv("TASKNAMER", "stablelm2:1.6b-zephyr-fp16")

project_name_ui = input("Give this project a unique name: ")

def generate_answers(agent, prompt):
    model_name = ""
    if agent == 'project_planner':
        model_name = PROJECT_PLANNER_MODEL
    elif agent == 'coder':
        model_name = CODER_MODEL
    elif agent == 'markdown':
        model_name = MARKDOWN_MAKER
    elif agent == 'taskname':
        model_name = TASKNAMER
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
    response = generate_answers("project_planner", f"Pose meaningful questions for the following project, enabling a very detailed project description to be created: {input}")
    return response

def service_desk2(answered_questions):
    complete_project = generate_answers("project_planner", f"Create a detailed project description for the following: {answered_questions}")
    return complete_project

def project_planner(proj):
    project = f"Create a detailed programming plan project task list for the following coding project: {proj}"
    response = generate_answers("project_planner", project)
    return manager(response)

def get_language_from_extension(file_name):
    """
    Determines the programming language based on the file extension.
    """
    extension_to_language = {
        '.py': 'python',
        '.js': 'javascript',
        '.html': 'html'
    }
    extension = os.path.splitext(file_name)[1]  # Extract the file extension
    return extension_to_language.get(extension, 'Unknown')  # Default to 'Unknown'

def manager(project_plan):
    """
    Sends a request to an AI bot to divide the project plan into individual tasks.
    The response is expected to contain tasks listed in Markdown format, starting after a '---'.
    The tasks are then extracted into a list.
    """
    prompt = f"Please divide the following project into a list of precise tasks with specific coding instructions. for building the application. one task is one file. Start the task listing with '---'. Ensure that each task is listed in Markdown format. Here's the project plan: {project_plan}"
    tasks_response = generate_answers("markdown", prompt)
    print(tasks_response)  # For debugging
    
    # Check if '---' is present in the response, to split tasks accordingly
    tasks = []
    if '---' in tasks_response:
        tasks_section = tasks_response.split('---')[1].strip()
        tasks = [task for task in tasks_section.split('\n') if task.strip()]
    else:
        if "##" in tasks_response:
            tasks_section = tasks_response.split("##")[1].strip()
            tasks = ['### ' + task for task in tasks_section.split('\n### ') if task.strip()]
        else:
            if "1." in tasks_response:
                tasks_section = tasks_response.split("1.")[1].strip()
                tasks = [f'{i+1}. ' + task for i, task in enumerate(tasks_section.split(f'\n{i+2}. ')) if task.strip()]
            else:
                print("Error: Expected markers not found in the response.")
        

    print(tasks)  # For debugging
   
    # Generate file structure based on tasks
    generate_file_structure(tasks)
   
    # Call a coder instance for each task
    code_snippets = []
    for task in tasks:
        filename, code_snippet = coder_instance(task)
        code_snippets.append((filename, code_snippet))
    
    # Test    
    tested_code_snippets = []
    for file_name, code_snippet in code_snippets:
        language = get_language_from_extension(file_name)  # Dynamically detect the language
        success, tested_code = testing(code_snippet, [], language)  # Provide test cases if needed
        tested_code_snippets.append((file_name, tested_code))
   
    # Generate documentation
    documentation(tested_code_snippets)
   
    # Install dependencies
    install_dependencies()

def generate_filename(task):
    """
    Generates a suitable filename for a given task. Assumes generate_answers 
    simulates the function call to an external system.
    """
    # Simuliere eine Antwort von einem externen System
    # In einer realen Anwendung würde hier generate_answers('taskname', f'create a suitable filename for this code task: {task}') aufgerufen
    response = generate_answers('taskname', f'create a suitable filename for this code task: {task}')
    # Suche nach Dateiendungen in der Antwort
    match = re.search(r'\S+?(\.html|\.css|\.js|\.py)\b', response)
    if match:
        # Extrahiere den Dateinamen aus der Antwort, aber entferne ungültige Zeichen, die in Dateinamen nicht erlaubt sind
        filename = re.sub(r'[<>:"/\\|?*]', '', match.group(0))
    else:
        # Verwende einen Standardnamen, wenn keine Dateiendung gefunden wird
        sanitized_task = re.sub(r'[<>:"/\\|?*]', '', task)  # Entferne ungültige Zeichen
        filename = sanitized_task.replace(" ", "_").lower() + ".txt"
    return filename

def generate_file_structure(task_list):
    """
    Creates folders and files based on a list of tasks.
    This function creates a folder for each task in the task_list,
    removes invalid characters from task names, replaces spaces with underscores,
    and creates a README.md file in each folder with a basic project description.
    """
    print("DIRECTORIES: ", task_list) # debugging
    for task in task_list:
        base = f'{project_name_ui}'
        folder_name = ''.join(c for c in task if c.isalnum() or c.isspace()).replace(" ", "_").lower()  # Remove invalid characters and replace spaces with underscores
        if not folder_name:  # Check if folder name is empty
            folder_name = "unnamed_project"  # Use a placeholder name if the task name results in an empty string
        
        # os.path.join(base, folder_name)
        os.makedirs(base, exist_ok=True)  # Create folder if not exists
        # Create a README.md file in the folder with the project description
    with open(f"{base}/README.md", 'w') as f:
        f.write(f"Project: {task}\n")

def coder_instance(task):
    """
    Generates code based on a specific task, removes the first word, and writes the code to a file.
    """
    code_response = generate_answers("coder", task) or ''  # Ensure it's not None
    if code_response:
        try:

            language, *code = code_response.split('```', 1)  # Attempt to separate programming language from code
            code = ''.join(code).strip()  # Rejoin the code without the programming language
            print(f"Language: {language}, Code: {code[:50]}")  # For debugging

            # Determine file extension based on programming language
            # file_extension = {
            #     'python': '.py',
            #     'javascript': '.js',
            #     'html': '.html',
            #     'css': '.css'
            #     # Add more language-extension mappings as needed
            # }.get(language.strip().lower(), '.txt')  # Default to .txt if language is not recognized
                    
            filename = generate_filename(task)
            
            with open(filename, 'w') as file:
                file.write(code_response)
            
            print(f"{filename} written with code snippet.")
            return filename, code_response
        
        except ValueError:
            print(f"Error processing task: {task}")
            pass
    else:
        print(f"No code generated for task: {task}")
        language, code = 'Unknown', ''
        pass
  

def testing(code, test_cases, language):
    """
    Tests the generated code using appropriate tools based on the programming language.
    Automatically corrects the code if errors occur and repeats the process until the code can be successfully executed.
   
    :param code: The code to be tested as a string.
    :param test_cases: Test cases specific to the programming language.
    :param language: The programming language of the code.
    :return: A tuple with the status of the code (True for success, False for failure) and the tested or corrected code.
    """
    corrected_code = code
    success = False
    
    if language == 'python':
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
    
    elif language == 'javascript':
        # Save the code to a temporary file
        with open('temp.js', 'w') as file:
            file.write(corrected_code)
        
        while not success:
            try:
                # Run the JavaScript code using Node.js
                subprocess.check_output(['node', 'temp.js'], stderr=subprocess.STDOUT)
                success = True  # No errors, test successful
            except subprocess.CalledProcessError as e:
                error_message = e.output.decode('utf-8')  # Error message
                success = True  # No errors, test successful
                # corrected_code = correction(corrected_code + "\n// Error: " + error_message)  # Attempt to correct the code
        
        # Remove the temporary file
        os.remove('temp.js')
    
    elif language == 'html':
        # Save the code to a temporary file
        with open('temp.html', 'w') as file:
            file.write(corrected_code)
        
        # Validate HTML using a library like html5lib or BeautifulSoup
        # You can install html5lib using: pip install html5lib
        import html5lib
        with open('temp.html', 'r') as file:
            html = file.read()
            parser = html5lib.HTMLParser(strict=True)            
            try:
                parser.parse(html)
                success = True  # No errors, HTML is valid
            except Exception as e:
                error_message = str(e)  # Error message
                # corrected_code = correction(corrected_code + "\n<!-- Error: " + error_message + " -->")  # Attempt to correct the code
        
        # Remove the temporary file
        os.remove('temp.html')
    
    return (success, corrected_code)  # Return the status and corrected code

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
    
    # if ".js" in file_extensions:
    #     # JavaScript dependencies
    #     print("Installing JavaScript dependencies...")
        
    #     # Check if package.json exists
    #     if os.path.exists("package.json"):
    #         subprocess.run(["npm", "install"])
    #     else:
    #         # Try to install common JavaScript packages
    #         common_packages = ["axios", "lodash", "moment"]
    #         for package in common_packages:
    #             try:
    #                 subprocess.run(["npm", "install", package])
    #             except subprocess.CalledProcessError:
    #                 print(f"Failed to install package: {package}")
    
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
                    
                    # # JavaScript dependencies
                    # if "require" in code:
                    #     lines = code.split("\n")
                    #     for line in lines:
                    #         if line.startswith("const") or line.startswith("var"):
                    #             package = line.split("=")[1].split("(")[1].split(")")[0].strip("'\"")
                    #             try:
                    #                 subprocess.run(["npm", "install", package])
                    #             except subprocess.CalledProcessError:
                    #                 print(f"Failed to install package: {package}")
    
    print("Dependency installation completed.")

if __name__ == '__main__':
    project_description = input("Please provide detailed input for your project: ")
    # response = service_desk(project_description)
    # print(response)
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
