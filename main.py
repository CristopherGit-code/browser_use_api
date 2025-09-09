from util.browser.browser_agent import BrowserUseAgent
import asyncio
import webbrowser

async def main():
    bwsr_agent = BrowserUseAgent()
    query = input("USER:")
    response = await bwsr_agent.use_browser(query)
    finsl_result = response.final_result()
    url_lists = response.urls()
    final_url = url_lists[-1]
    duration = response.total_duration_seconds()
    webbrowser.open(final_url)

if __name__ == "__main__":
    asyncio.run(main())