# Common imports
import os
from dotenv import load_dotenv
import json
# import lolviz
from openai import OpenAI
from langchain.agents import Tool
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
import streamlit as st

# Import the key CrewAI classes
from crewai import Agent, Task, Crew


# Load the environment variables
# If the .env file is not found, the function will return `False
if load_dotenv('.env'):
   # for local development
   OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else:
   OPENAI_KEY = st.secrets['OPENAI_API_KEY']

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# After loading the environment variables, we can access them using the `os` module,
# e.g., `os.getenv('OPENAI_API_KEY')`

# Code below prints out the truncated OPENAI_API_KEY
# print(f'OPENAI_API_KEY = "{os.getenv('OPENAI_API_KEY')[:20]}"')
print(OPENAI_KEY)

# print(f'OPENAI_MODEL_NAME = "{os.getenv('OPENAI_MODEL_NAME')}"')

os.environ['OPENAI_MODEL_NAME'] = "gpt-4o-mini"

# read csv
path ='./data'
extension = '.csv'

files = [file for file in os.listdire(path) if file.endswith(extension)]
dfs_raw = []
for file in files:
   df_raw = pd.read_csv(os.path.join(path, file), low_memory=False)
   dfs_raw.append()

# combine raw table
df = pd.concat(dfs_raw, ignore_index=True)

# csvpath = './data/hdb_resale_full_with_mall_hawker.csv'
# df = pd.read_csv(csvpath)

pandas_tool_agent = create_pandas_dataframe_agent(
    llm=ChatOpenAI(temperature=0, model='gpt-4o-mini'),
    df=df,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True # <-- This is an "acknowledgement" that this can run potentially dangerous code
)

# Create the tool
pandas_tool = Tool(
    name="Manipulate and Analyze tabular data with Code",
    func=pandas_tool_agent.invoke, # <-- This is the function that will be called when the tool is run. Note that there is no `()` at the end
    description="Useful for search-based queries",
)


from crewai_tools import WebsiteSearchTool

# Create a new instance of the WebsiteSearchTool
# Set the base URL of a website, e.g., "https://example.com/", so that the tool can search for sub-pages on that website
tool_websearch = WebsiteSearchTool("https://www.hdb.gov.sg/")


# Creating Agents
agent_data_analyst = Agent(
    role="Data Analyzer",
    goal="Analyze the data based on user query: {topic}",
    backstory="""You're the best data analyst.
    You are working with information of resale flat transaction for housing development board (HDB) singapore and you will use the information to answer user query""",
    allow_delegation=False,
	verbose=True,
    tools=[pandas_tool],
)

agent_researcher = Agent(
    role="Research Analyst",
    goal="Conduct research on the topic: {topic}",
    backstory="""You're working on conducting in-depth research on the topic: {topic}.
    You have access to web search tools and other resources to gather the necessary information.""",
    # You will provide the Content Planner with the latest trends, key players, and noteworthy news on the topic. <-- This line is removed.
    # Based on the request that Content Planner, you will provide additional insights and resources from reliable and credible websites.""", <-- This line is removed.
    allow_delegation=False,
    verbose=True,
)

agent_writer = writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate response based on user query: {topic}",

    backstory="""You're working on a writing a insightful and factual response based on user query: {topic}.
    You base your writing on the outline from Data Analyzer and the research report from the Research Analyst.""", # <-- New line added
    # You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic.  <-- This line is removed.
    # You follow the main objectives and direction of the outline as provide by the Content Planner.""",  <-- This line is removed.

    allow_delegation=False,
    verbose=True,
)

# agent_planner = Agent(
#     role="Content Planner",

#     goal="Plan engaging and factually accurate content on {topic}",

#     backstory="""You're working on planning a blog article about the topic: {topic}."
#     You collect information that helps the audience learn something about the topic and make informed decisions."
#     Your work is the basis for the Content Writer to write an article on this topic.""",

#     allow_delegation=False, # we will explain more about this later

# 	verbose=True, # to allow the agent to print out the steps it is taking
# )

# agent_writer = writer = Agent(
#     role="Content Writer",

#     goal="Write insightful and factually accurate opinion piece about the topic: {topic}",

#     backstory="""You're working on a writing a new opinion piece about the topic: {topic}.
#     You base your writing on the work of the Content Planner, who provides an outline and relevant context about the topic.
#     You follow the main objectives and direction of the outline as provide by the Content Planner.""",

#     allow_delegation=False, # we will explain more about this later

#     verbose=True, # to allow the agent to print out the steps it is taking
# )

task_analyze = Task(
    description="""\
    1. Understand the user query: {topic}.
    2. Use the tool to analyze the data based on the user query.
    3. Develop a comprehensive report based on the analysis.""",

    expected_output="""\
    A comprehensive analysis report that present the results using McKinsey's Pyramid Principle.""",

    agent=agent_data_analyst,
    async_execution=True # Will be executed asynchronously [NEW]
)

task_research = Task(
    description="""\
    1. Conduct in-depth research user query: {topic}.
    2. Provide the Content Writer with the latest trends, key players, and noteworthy news on the topic.""",

    expected_output="""\
    A detailed research report with the latest trends, key players, and noteworthy news on the topic.""",

    agent=agent_researcher,
    tools=[tool_websearch],

    async_execution=True # Will be executed asynchronously [NEW]
)

task_write = Task(
    description="""\
    1. Use the content plan to craft a factually correct response on {topic} based on user query.
    2. Reply should be accurate and succint.""",

    expected_output="""
    A well-written and factually correct response to answer user query, each response should be succint.""",
    agent=agent_writer,
    # human_input=True, # Remove user input for this task [NEW]

    context=[task_analyze, task_research], # Will wait for the output of the two tasks to be completed,
    output_file="article.md" # <-- This allows the output of this task to be saved to a file [NEW]
)


# task_plan = Task(
#     description="""\
#     1. Prioritize the latest trends, key players, and noteworthy news on {topic}.
#     2. Identify the target audience, considering "their interests and pain points.
#     3. Develop a detailed content outline, including introduction, key points, and a call to action.""",

#     expected_output="""\
#     A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources.""",

#     agent=agent_planner,
# )

# task_write = Task(
#     description="""\
#     1. Use the content plan to craft a compelling blog post on {topic} based on the target audience's interests.
#     2. Sections/Subtitles are properly named in an engaging manner.
#     3. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.
#     4. Proofread for grammatical errors and alignment the common style used in tech blogs.""",

#     expected_output="""
#     A well-written blog post "in markdown format, ready for publication, each section should have 2 or 3 paragraphs.""",

#     agent=agent_writer,
# )

# Creating the Crew
# crew = Crew(
#     agents=[agent_data_analyst],
#     tasks=[task_analyze],
#     verbose=True
# )

crew = Crew(
    agents=[agent_data_analyst, agent_writer],
    tasks=[task_analyze, task_write],
    verbose=True
)

# Running the Crew
# result = crew.kickoff(inputs={"topic": "How many resale transaction in trans_year 2020?"})
# result = crew.kickoff(inputs={"topic": "What is the procedure for buying an resale hdb?"})
# print(result.raw)
def generate_answer(topic):
    result = crew.kickoff(inputs={"topic": topic})
    return result.raw
# user_prompt = "How many resale transaction in trans_year 2020?"
# generate_answer(user_prompt)

# crew = Crew(
#     agents=[agent_planner, agent_writer],
#     tasks=[task_plan, task_write],
#     verbose=True
# )

# # Start the crew's task execution
# result = crew.kickoff(inputs={"topic": "Large Language Models"})