from util.oci_openai_client import LLM_Open_Client
from browser_use import Agent
from util.langchain.chat import ChatLangchain
from browser_use import Agent, Browser, BrowserProfile
from dotenv import load_dotenv
load_dotenv()
import asyncio
from util.config.config import Settings

settings = Settings(r"C:\Users\Cristopher Hdz\Desktop\Test\browser_api\util\config\config.yaml")
didactic_user = settings.credentials.DIDACTIC_USER
didactic_pass = settings.credentials.DIDACTIC_PASSWORD
dict_pass = didactic_pass[1:]

browser = Browser(
    headless=False,
    window_size={'width':1000,'height':700},
    allowed_domains=['*google.com','didactic.uaslp.mx'],
)

browser_profile = BrowserProfile(
    allowed_domains=['*google.com','didactic.uaslp.mx'],
    enable_default_extensions=False
)

# sensitive_data = {'Clave unica':didactic_user,'Contrasegna institucional':dict_pass}

async def main():
    oci_langchain_client = LLM_Open_Client().build_llm_client()

    llm = ChatLangchain(
		chat=oci_langchain_client
	)
    
    task = "Go to youtube.com and find a cool song from 'coldplay'"
	
    agent = Agent(
        task=task,
        # browser=browser,
        # browser_profile=browser_profile,
        # sensitive_data=sensitive_data,
        llm=llm
    )

    history = await agent.run()
    
    print(f'✅ Task completed! Steps taken: {len(history.history)}')
    
    if history.final_result():
        print(f'📋 Final result: {history.final_result()}')
        return history

if __name__ == "__main__":
    asyncio.run(main())