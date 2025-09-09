import gradio as gr
from util.browser.browser_agent import BrowserUseAgent
from util.browser.browser_tools import BrowserAgentTools

tool_watcher = BrowserAgentTools()

async def use_browser(query,message_history):
    bwsr_agent = BrowserUseAgent()
    prompt = query + " Solve the previous query. If the query is not clear, ask the user for clarification"
    response = await bwsr_agent.use_browser(prompt)
    final_result = response.final_result()
    url_lists = response.urls()
    final_url = url_lists[-1]
    duration = response.total_duration_seconds()
    return final_result

with gr.Blocks() as browser_app:
    gr.Markdown("""<h1 align="center"> Browser app </h1>""")

    gr.ChatInterface(
        fn=use_browser, 
        chatbot=gr.Chatbot(height=500, placeholder='Browser chat' ,type='messages',render_markdown=True),
        type="messages",
    )

    asking_help = gr.Textbox(interactive=False,label="AI is requesting help with this:")
    user_response = gr.Textbox(placeholder="The response to the agent question is...",label="Type your response:")

    gr.Timer(value=0.5).tick(
        fn=tool_watcher.update_question,
        inputs=[],
        outputs=[asking_help]
    )

    user_response.submit(
        tool_watcher.update_human_response,
        inputs=[user_response],
        outputs=[user_response,asking_help]
    )

if __name__=='__main__':
    browser_app.launch(show_api=False)