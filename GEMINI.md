# Gemini A2A Agent Development Guide

This document provides instructions and best practices for building and refactoring A2A (Agent-to-Agent) agents, based on the structure and functionality of the sample agent in this directory.

## Project Structure

A typical A2A agent project should have the following structure:

```
.
├── agent_executor.py
├── deploy.sh
├── gemini_agent.py
├── main.py
├── Procfile
├── README.md
└── requirements.txt
```

- **`gemini_agent.py`**: Contains the core logic of the agent, including the agent's tools, prompts, and the main `GeminiAgent` class.
- **`main.py`**: The entry point of the application. This file is responsible for creating and running the web server that exposes the agent's functionality.
- **`agent_executor.py`**:  Handles the execution of the agent's tasks, including managing the agent's lifecycle and handling requests.
- **`requirements.txt`**: Lists all the Python dependencies required for the project.
- **`deploy.sh`**: A script containing the necessary commands to deploy the agent to a cloud environment.
- **`README.md`**: Provides a general overview of the project.
- **`Procfile`**:  Declares the commands to be executed by the application on a deployment platform (e.g., Heroku, Google App Engine).

## Core Components

### `gemini_agent.py`

This is the heart of your agent. It should contain a class, typically named `GeminiAgent`, that encapsulates the agent's functionality. This includes:

- **Initialization**: The constructor should initialize the agent's tools, prompts, and any other required resources.
- **Tools**: Define the tools that the agent can use to interact with its environment.
- **Prompts**: Craft the prompts that guide the agent's behavior.

### `main.py`

This file is the application's entry point. It should:

1.  Create an instance of the `GeminiAgent`.
2.  Create an instance of the `AgentExecutor`, passing the `GeminiAgent` instance to it.
3.  Create a web server (e.g., using Flask or FastAPI) and define the routes that will handle requests to the agent.
4.  Start the web server.

### `agent_executor.py`

This component is responsible for the execution of the agent's tasks. It should:

-   Receive requests from the web server.
-   Invoke the `GeminiAgent` to process the requests.
-   Handle the agent's lifecycle, including initialization and shutdown.
-   Return the agent's responses to the web server.

## Dependencies

All Python dependencies should be listed in the `requirements.txt` file. To install the dependencies, run:

```bash
pip install -r requirements.txt
```

## Deployment

The `deploy.sh` script should contain the commands to deploy the agent. This may include:

-   Installing dependencies.
-   Running database migrations.
-   Starting the application server.

The `Procfile` specifies the commands that are run by the application's dynos on platforms like Heroku. For example:

```
web: gunicorn main:app
```

This command tells the platform to start a `gunicorn` server, running the `app` object from the `main.py` file.

## Refactoring Guide

When refactoring existing code to create an A2A agent, follow these steps:

1.  **Identify the Core Logic**: Isolate the code that contains the core functionality of the agent. This will be the basis for your `GeminiAgent` class.
2.  **Separate Concerns**: Refactor the code to separate the agent's core logic from the web server and execution logic.
    -   Move the agent's core logic to `gemini_agent.py`.
    -   Move the web server code to `main.py`.
    -   Move the agent execution logic to `agent_executor.py`.
3.  **Define Tools and Prompts**: Clearly define the agent's tools and prompts within the `GeminiAgent` class.
4.  **Manage Dependencies**: Create a `requirements.txt` file and list all the necessary dependencies.
5.  **Create Deployment Scripts**: Create a `deploy.sh` script and a `Procfile` to automate the deployment process.
