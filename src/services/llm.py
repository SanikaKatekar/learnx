import re
import ast
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class LLMHelper:
    def __init__(self, payload):
        self.topic = payload.topic #user input 
        self.level = payload.level #user input - (beginner, intermediate, advanced)
        self.model = ChatOpenAI(openai_api_key=payload.openai_api_key) #initialize the model

    # function to generate learning plan or study plan
    def generate_learning_plan(self, knowledge_base):
        #Create a template string for the prompt to be sent to LLM
        template_string = """
        Task: Generate a Structured Study/Learning Plan.

        Objective: Create a structured study/learning plan for a specified topic, taking into account the user's study level. This should be designed to assist users in planning their study approach efficiently.

        Instructions:
        Use the below user information to create the plan for the user. Assume the user has access to information in the form of web articles.
        1. {topic}: The topic for which the user needs a study plan.
        2. {level}: Whether the user is a beginner, amateur, or advanced in this subject matter.

        Output Response Template:
        1. Chapter 1: Introduction to [topic]
        - Subtopics or concepts to cover:
            - [Subtopic 1]
            - [Subtopic 2]
            - [Subtopic 3]
        2. Chapter 2:
        - Subtopics or concepts to cover:
            - [Subtopic 4]
            - [Subtopic 5]
        3. Chapter 3:
        - Subtopics or concepts to cover:
            - [Subtopic 6]
            - [Subtopic 7]
            
        Important Note: Continue this structure for the entire study plan, extending for further chapters. Please generate the structured learning plan directly without additional questions. Ensure that the output response includes a structured learning plan tailored to the user's study level. Use the provided output response template as a guideline for consistency.

        Feel free to use the provided topic information below to make a detailed and curated study/learning plan:
        Topic Information: ```{text}```
        """
        #Create prompt
        prompt_template = ChatPromptTemplate.from_template(template_string)
        prompt_messages = prompt_template.format_messages(
                            topic=self.topic,
                            level=self.level,
                            text=knowledge_base)
        # Call the LLM 
        llm_response = self.model(prompt_messages)
        return llm_response

    #Function to create dictionary of the learning path from the LLM's response. 
    def create_dictionary_from_string(self, input_string):
        template_string_for_json = """
        From the given string create a dictionary of chapters as key and the list of subtopics as value.
        STRING: {string}
        """
        prompt_template_for_json = ChatPromptTemplate.from_template(template_string_for_json)
        prompt_messages_for_json = prompt_template_for_json.format_messages(string=input_string)
        # Call the LLM 
        llm_response = self.model(prompt_messages_for_json)
        return llm_response

    #Function to extract dictionary from the above LLM's response.
    def extract_dictionary_from_content(self, content):
        # Use regular expression to find the dictionary portion
        pattern = r'{[^{}]*}'
        # Find the matching dictionary using regex
        match = re.search(pattern, content)
        if match:
            # Extract the matched dictionary string
            dictionary_str = match.group(0)
            try:
                # Convert the dictionary string to a Python dictionary using `ast.literal_eval()`
                dictionary = ast.literal_eval(dictionary_str)
                return dictionary
            except Exception as e:
                print(f"Error converting dictionary string to Python dictionary: {e}")
                return None
        else:
            print("No dictionary found in the input string.")
            return None
        
    # Function to wrap everything together and get the final learning plan in the form of a dictionary from the LLMs
    def get_learning_plan(self, knowledge_base):
        # get study plan as a string from the llm
        llm_response = self.generate_learning_plan(knowledge_base)
        # create a dictionary of the plan. 
        llm_dict = self.create_dictionary_from_string(llm_response.content)
        # convert the string into dictionary type
        final_dict = self.extract_dictionary_from_content(llm_dict.content)
        return final_dict
    
    # Function to generate the quiz
    def generate_quiz(self, final_dict, knowledge_base):
        # template string for llm
        template_string_for_quiz = """Generate a quiz on {topic} with 10-15 multiple choice questions (3-4 answer options). You can use the following topic information and study/learning plan:
        topic information:
        {knowledge_base}

        Study/Learning Plan:
        {learning_plan}

        Important Note: The quiz should roughly evaluate the study/learning plan. Also give the correct answer key for the quiz at the end.
        """
        # prompt template 
        prompt_template_for_quiz = ChatPromptTemplate.from_template(template_string_for_quiz)
        prompt_messages_for_quiz = prompt_template_for_quiz.format_messages(
            topic=self.topic,
            learning_plan=final_dict,
            knowledge_base=knowledge_base)
        # call the llm
        quiz_response = self.model(prompt_messages_for_quiz)
        return quiz_response.content