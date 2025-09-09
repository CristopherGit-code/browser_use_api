from browser_use import Tools, ActionResult
from time import sleep

tools = Tools()

@tools.action(description="Ask human for help with a question")
def ask_human(question:str)->ActionResult:
    tool_watcher = BrowserAgentTools()
    tool_watcher.ai_question = question
    tool_watcher.human_response = None
    answer = tool_watcher.get_human_responses()
    return f'The human responded with: {answer}'

class BrowserAgentTools:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserAgentTools,cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.ai_question = None
            self.human_response = None
            BrowserAgentTools._initialized = True

    def update_question(self):
        return self.ai_question
    
    def update_human_response(self,response = 'No action need'):
        self.human_response = response
        return "","Response received"
    
    def get_human_responses(self):
        while not self.human_response:
            print("waiting for response")
            sleep(2)
        return self.human_response