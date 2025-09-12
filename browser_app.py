import gradio as gr
from util.browser.browser_agent import BrowserUseAgent
from util.browser.browser_tools import BrowserAgentTools

tool_watcher = BrowserAgentTools()

async def use_browser(query,message_history):
    user = "example"
    password = "pass"
    bwsr_agent = BrowserUseAgent(user,password)
    prompt = f""" You are a browser agent in charge of solving the user request: {query}. 
    There is this context availabe from previous user-agent interaction and conversations: {message_history}. 
    Using the context, address the user query, use the browser tools to look for information and gather data.
    You can also request the user for help in case there is a not clear step, or if there is extra details / information needed to complete the tastk.
    """
    response = await bwsr_agent.use_browser(prompt)
    final_result = response.final_result()
    url_lists = response.urls()
    final_url = url_lists[-1]
    duration = response.total_duration_seconds()
    return final_result

with gr.Blocks() as browser_app:
    gr.Markdown("""<h1 align="center"> Browser app </h1>""")

    with gr.Tab("Browser agent"):
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

    with gr.Tab("Secret keys"):
        user = gr.Textbox(label="Site user")
        password = gr.Textbox(label="Site password")
        system_instructions = gr.Textbox(label="System instructions")

if __name__=='__main__':
    browser_app.launch(show_api=False)