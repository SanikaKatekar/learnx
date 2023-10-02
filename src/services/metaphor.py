from bs4 import BeautifulSoup
from metaphor_python import Metaphor


class MetaphorHelper:
    def __init__(self, payload):
        self.topic = payload.topic # user input
        self.level = payload.level #user input - (beginner, intermediate, advanced)
        self.metaphor = Metaphor(payload.metaphor_api_key) #initialize

    # Using the Metaphor API Search functionality to get links about a certain topic
    def get_topic_links(self):
        # Define your query 
        query = f"Latest articles on for learning {self.topic} for {self.level} level."
        # Send a search request to the Metaphor API
        search_response = self.metaphor.search(
            query=query,
            num_results=5,  # You can adjust the number of results as needed
            use_autoprompt = True # auto prompting set to True for better query generation
        )
        return search_response

    # Using the Metaphor API Getcontents functionality to get the information from the links
    def get_content_for_topic(self, response):
        content_response_list = []
        if response.results:
            for result in response.results:
                # Get the HTML content for the URL
                content_response = self.metaphor.get_contents([result.id])
                content_response_list.append(content_response)
            print("Content retrieved and stored.")
        else:
            print("No content found for this topic.")
            print()  # Add an empty line for readability
        return content_response_list

    # Function to extract text from HTML and update 'Extract' key
    def extract_text_from_html(self, content_response_list):
        for item in content_response_list:
            try:
                # Access the 'extract' attribute within the 'DocumentContent' object
                html = item.contents[0].extract
                soup = BeautifulSoup(html, 'html.parser')
                item.contents[0].extract = soup.get_text()  # Update the 'extract' attribute
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        return content_response_list

    # Function to create one knowledge base from the gathered information
    def create_knowledge_base(self, content_response_list):
        knowledge_base = ""
        for contents in content_response_list:
            knowledge_base += str(contents.contents[0].extract) # keep only the contents from the 'extract' key
        return knowledge_base
    
    # Function to wrap everything together and get the final knowledge base
    def get_knowledge_base(self):
        # Use Metaphor API's Search to get latest article links
        response = self.get_topic_links()
        # Get contents from the links by using Metaphor API's get_content()
        content_response_list = self.get_content_for_topic(response)
        # Extract text from HTML 
        content_response_list = self.extract_text_from_html(content_response_list)
        # Create a final knowledge base 
        knowledge_base = self.create_knowledge_base(content_response_list)
        return knowledge_base

    # Function to search for links related to a subtopic using Metaphor API
    def search_links_for_subtopic(self, subtopic):
        # Make a search API call for the subtopic and get 3 links
        search_result = self.metaphor.search(subtopic, num_results=3)  # You can adjust the number of results as needed
        # Extract and return the links as a list
        return [result.url for result in search_result.results]

    # Function to populate the dictionary with links for each chapter and subtopic
    def populate_links_dictionary(self, resulting_dictionary):
        new_resulting_dictionary = {}
        # Get three links for each sub-topic in each chapter
        for chapter, subtopics in resulting_dictionary.items():
            subtopic_links = {}
            for subtopic in subtopics:
                links = self.search_links_for_subtopic(subtopic)
                subtopic_links[subtopic] = links
            #append to the dictionary
            new_resulting_dictionary[chapter] = subtopic_links
        return new_resulting_dictionary