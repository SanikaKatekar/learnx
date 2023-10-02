from services.metaphor import MetaphorHelper
from services.llm import LLMHelper
from api.payloads.payloads import RequestPayload

class GetStudyPlan:
    def __init__(self, payload: RequestPayload):
        self.payload = payload # user inputs
        self.metaphor = MetaphorHelper(payload) # Metaphor Helper class
        self.llm = LLMHelper(payload) # LLM Helper class

    def generate_plan(self):
        try:
            # Creating the knowledge base using Metaphor API functions
            kb = self.metaphor.get_knowledge_base()
            # Using the LLM to generate a personalized learning plan/study plan
            study_plan_dict = self.llm.get_learning_plan(kb)
            # Using Metaphor API to get links and resources for the topics in the generated learning path
            study_plan_dict_links = self.metaphor.populate_links_dictionary(study_plan_dict)
            # Generate a customized quiz on the topic as final assesment
            quiz = self.llm.generate_quiz(study_plan_dict, kb)
            ## Final Response
            study_plan = {
            "Study Plan": study_plan_dict_links,
            "Quiz": quiz,
            }
            return study_plan
        except Exception as e:
            return {"Service Status": "Failed", "Error": e}