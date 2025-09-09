from util.openai_client import LLM_Open_Client
from browser_use import Agent
from util.langchain.chat import ChatLangchain
from browser_use import Agent, Browser, BrowserProfile
from dotenv import load_dotenv
load_dotenv()
from util.config.config import Settings
from util.browser.browser_tools import tools

class BrowserUseAgent:
    def __init__(self):
        self._settings = Settings(r"C:\Users\Cristopher Hdz\Desktop\Test\browser_api\util\config\config.yaml")
        self.sensitive_data = {'Clave unica':'example user','Contrasegna institucional':'dict_pass'}
        self._browser = Browser(
            headless=False,
            window_size={'width':500,'height':700},
            allowed_domains=['*google.com','didactic.uaslp.mx'],
        )
        self._browser_profile = BrowserProfile(
            allowed_domains=['*google.com','didactic.uaslp.mx'],
            enable_default_extensions=False,
        )
        self._oci_langchain_client = LLM_Open_Client().build_llm_client()
        self._browser_llm = ChatLangchain(
            chat=self._oci_langchain_client
        )
        self.tools = tools

    async def use_browser(self,task:str):
        agent_task = task
        
        agent = Agent(
            task=agent_task,
            llm=self._browser_llm,
            tools=self.tools
        )
        
        history = await agent.run()
    
        if history.final_result():
            return history