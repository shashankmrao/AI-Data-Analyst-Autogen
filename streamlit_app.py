import os
import asyncio
import streamlit as st
from teams.data_analyst import getDataAnalyzerTeam
from models.groq_model_client import get_model_client
from utils.docker_util import getDockerCommandLineExecutor,start_docker_container,stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.title('Digital Data Analyzer')
uploaded_file=st.file_uploader("Upload a csv file",type=["csv"])

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None
if('images_shown') not in st.session_state:
    st.session_state.images_shown=[]

task=st.chat_input("Enter your task here...")

async def run_analyser_gpt(docker,groq_model_client,task):
    try:
        await start_docker_container(docker)
        team=getDataAnalyzerTeam(docker,groq_model_client)
        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)
        
        async for message in team.run_stream(task=task):
            if isinstance(message,TextMessage):
                if message.source.startswith('user'):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(message.content)
                elif message.source.startswith('Data_Analyzer_agent'):
                    with st.chat_message('Data Analyzer',avatar='🤖'):
                        st.markdown(message.content)
                elif message.source.startswith('Python_Code_Executor'):
                    with st.chat_message('Code Executor',avatar='👨‍💻'):
                        st.markdown(message.content)
                st.session_state.messages.append(message.content)
            elif isinstance(message,TaskResult):
                st.markdown(f'Stop Reason: {message.stop_reason}')
                st.session_state.messages.append(message.stop_reason)
            
        st.session_state.autogen_team_state= await team.save_state()

        return None
    except Exception as e:
        st.error(f"Error": {e})
        return e
    finally:
        await stop_docker_container(docker)

async def do_something_big():
    await asyncio.sleep(1)

if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(msg)

if task:
    if uploaded_file is not None:
        if not os.path.exists('temp'):
            os.makedirs('temp',exist_ok=True)

        with open('temp/data.csv', 'wb') as f:
            f.write(uploaded_file.getbuffer())

        groq_model_client=get_model_client()
        docker=getDockerCommandLineExecutor()

        error = asyncio.run(run_analyser_gpt(docker,groq_model_client,task))

        if os.path.exists('temp/output.png'):
            st.image('temp/output.png')

    else:
        st.warning('Please upload the file and provide the task')

else:
    st.warning('Please provide the task')
