# LearnX: Personalized Learning with Metaphor API
LearnX is a project that addresses a critical challenge in education: keeping pace with the ever-evolving world of knowledge. In an era where Large Language Models (LLMs) like ChatGPT are changing how we learn, the LearnX project leverages the Metaphor API to create a dynamic learning platform. This platform offers personalized learning/study plans, ensuring users stay current with the latest developments without the hassle of resource hunting. LearnX excels in providing structured learning plans, filling the gap where users often struggle to find a well-organized study path amidst the vast sea of information available on the internet. Harnessing the latest LLMs using LangChain and Metaphor API technologies, LearnX is the key to efficient and structured learning.

## Project Structure

The LearnX project is implemented with FastAPI framework that generates structured study plans based on the user's topic of interest. The project is structured as follows:

-   `src/`: Contains the application code, including the FastAPI application setup, API routes, endpoints, and services.
-   `requirements/`: Contains the project dependencies.
-   `demo-notebook/`: Contains a jupyter notebook that serves as a comprehensive demonstration of LearnX's capabilities
-   `ReadME.md`: Contains the project documentation, including the usage instructions and the project structure.

## Functionality

To use the LearnX API, the user sends a POST request to the `/generate-study-plan` endpoint with the following payload:

```
{
  "topic": "string",
  "level": "string",
  "metaphor_api_key": "string",
  "openai_api_key": "string"
}
```

-   `topic` (required): The topic of study.
-   `level` (required): Learning level (beginner/intermediate/advanced).
-   `metaphor_api_key` (required): API key for Metaphor API.
-   `openai_api_key` (required): API key for OpenAI.

## Setup and Installation

1.  Clone the repository:

```
git clone https://github.com/SanikaKatekar/learnx.git
cd learnx
```

2.  Install dependencies:

```
pip install -r requirements/requirements.txt
```

## Usage

1.  Run  `python main.py`  in the  `learnx/src`  directory.

2.  Access the FastAPI Swagger UI at  `http://localhost:8000/docs`.

3.  Select the  `POST`  method for the  `/generate-study-plan`  endpoint.

4.  In the Request Body section, click the  `Try it out!`  button.

5.  Define the request body (payload) as shown in **Functionality** section, setting your values for the  `topic`,  `level`,  `metaphor_api_key`, and  `openai_api_key`  parameters.

6. Click the `Execute` button and the response will contain the generated study plan.

## Demo Notebook

Explore LearnX's capabilities with the self-contained Jupyter notebook, which can be accessed from the "demo-notebook" folder within the project root. This interactive environment allows you to execute LearnX's core functionality without the need to run the FastAPI application separately.