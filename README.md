> [!IMPORTANT]  
> ###### serves as a proof-of-concept for the simplicity of creating a full-stack dev by having ollama installed / access to ollama-models

# AIRO (Automated Idea Realization with Ollama)

AIRO is a practical tool designed to bridge the gap between conceptual ideas and real-world software applications. By leveraging the Ollama framework, AIRO enables users to describe their software needs or project ideas in natural language. The system then interprets these descriptions to autonomously generate functioning code, making the first steps towards automated software development more accessible and straightforward.

## Features

- **Idea to Implementation** : Transform your application ideas into real, working software with minimal manual coding.
- **Local Model Execution** : AIRO utilizes the Ollama framework for efficient local execution of complex language models, ensuring privacy and speed.
- **Ease of Use** : Designed with simplicity in mind, users can start with just an idea and end up with a prototype or working application.

## How It Works

1. **Describe Your Project**: Use natural language to describe the functionality and requirements of your desired software.
2. **Automatic Code Generation**: AIRO processes your description, queries Ollama-based models, and generates the initial code base.
3. **Iterative Testing and Correction**: The generated code is tested; if issues are detected, AIRO automatically attempts to correct them until a stable version is achieved.
4. **Documentation and Further Steps**: AIRO can also assist in generating basic documentation and provide guidance for further development steps.

## Requirements

- Local server running the Ollama framework for language model interactions.
- Python environment for executing the provided scripts and managing dependencies.

## Code Overview

```python
import requests
import json
import os
import sys
import traceback
import ollama
import html5lib
import dotenv
import subprocess

# Functions like `generate_answers`, `servicedesk`, and `coderinstance` facilitate the interaction with Ollama models,
# manage project planning, code generation, and automatic correction of generated code.
```

install requirements via pip:
```pip
pip install ollama requests html5lib dotenv
