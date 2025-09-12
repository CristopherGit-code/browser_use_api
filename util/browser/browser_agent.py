from util.oci_openai_client import LLM_Open_Client
from browser_use import Agent
from util.langchain.chat import ChatLangchain
from browser_use import Agent, Browser, BrowserProfile
from dotenv import load_dotenv
load_dotenv()
from util.config.config import Settings
from util.browser.browser_tools import tools

class BrowserUseAgent:
    def __init__(self,user,password):
        self._settings = Settings(r"C:\Users\Cristopher Hdz\Desktop\Test\browser_api\util\config\config.yaml")
        self._browser = Browser(
            headless=False,
            window_size={'width':600,'height':300},
            # allowed_domains=['*google.com'],
            keep_alive=True
        )
        self._browser_profile = BrowserProfile(
            allowed_domains=['*google.com'],
            enable_default_extensions=False,
        )
        self._oci_langchain_client = LLM_Open_Client().build_llm_client()
        self._browser_llm = ChatLangchain(
            chat=self._oci_langchain_client
        )
        # To inject the data, not passing to LLM
        self._sensitive_data = {"gmail_user":user,"gmail_password":password}
        self.tools = tools
        #TODO: Set to false to prevent AI from seeing screenshots of the password
        self._use_vision = True

    async def use_browser(self,task:str):
        agent_task = task
        
        agent = Agent(
            task=agent_task,
            llm=self._browser_llm,
            tools=self.tools,
            browser=self._browser,
            sensitive_data=self._sensitive_data,
            use_vision=self._use_vision
        )
        
        history = await agent.run()
    
        if history.final_result():
            return history