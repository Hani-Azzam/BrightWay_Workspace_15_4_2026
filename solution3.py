# Solution to Assignment 3 — "Ask-then-Introduce" (Short-Term Memory)
import os
from pprint import pprint

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_API_KEY : str = 'gemini-api-key'
GEMINI_MODEL_NAME : str = 'gemini-model-name'
GEMINI_TEMPERATURE : str = 'gemini-temperature'

ENV_GEMINI_API_KEY : str = 'GEMINI_API_KEY'
ENV_GEMINI_MODEL_NAME : str = 'GEMINI_MODEL_NAME'
ENV_GEMINI_TEMPERATURE : str = 'GEMINI_TEMPERATURE'

config: dict[str, object] = {
    GEMINI_API_KEY: os.getenv('GEMINI_API_KEY'),
    GEMINI_MODEL_NAME: os.getenv('GEMINI_MODEL_NAME', 'gemini-1.5-flash'),
    GEMINI_TEMPERATURE: float(os.getenv('GEMINI_TEMPERATURE', 0.0))
}

if not config[GEMINI_API_KEY]:
    raise RuntimeError(
        f"{GEMINI_API_KEY} environment variable is missing."
        "copy .env.example to .env and set your key."
    )

example_human_text1 : str =  """Full name: Sarah Cohen
 Role or degree: Data Analyst at FinSight Analytics
 Experience: 3 years
 top 3 Skills: SQL, Python, Power BI
 Major achievement: Built an automated dashboard that reduced reporting time by 80%
 Goal: Transition into a Data Scientist role focused on machine learning
 Optional fun fact: I'm obsessed with solving escape rooms"""
example_AI_text1 : str = """=== Your Introduction ===

Hi! I'm Sarah Cohen, a Data Analyst at FinSight Analytics with over three
years of experience turning messy data into meaningful insights.
I specialize in SQL, Python, and Power BI, and recently built an automated
dashboard that cut reporting time by 80%, freeing my team to focus on
strategy instead of spreadsheets.
I'm now eager to take the next step into a Data Scientist role where I can
apply machine learning to uncover deeper trends and drive smarter decisions.
Outside of work, you'll probably find me in an escape room, chasing clues
and time limits with the same curiosity I bring to every dataset.

TAG: sara.cohen@school.edu
"""
example_human_text2 : str = """Full name: Lior Ben-David
 Role or degree: Backend Engineer at CloudNova
 Experience: 5 years
 top 3 Skills: Python, Kubernetes, PostgreSQL
 Major achievement: Reduced API response time by 60% by redesigning the caching layer
 Goal: Lead a platform engineering team
 Optional fun fact: I built my own mechanical keyboard"""
example_AI_text2 : str = """=== Your Introduction ===

Hi! I'm Lior Ben-David, a Backend Engineer at CloudNova with five years of
experience building and scaling distributed systems.
I work primarily with Python, Kubernetes, and PostgreSQL, and recently
redesigned our caching layer — cutting API response times by 60% and
significantly improving user experience across the platform.
Looking ahead, I'm excited to step into a platform engineering leadership role
where I can mentor engineers while shaping the technical roadmap.
When I'm not optimising queries or container orchestration, you'll find me
soldering switches and building mechanical keyboards from scratch.

TAG: lior.ben-david@school.edu
"""

# create the template class
prompt_template : ChatPromptTemplate = ChatPromptTemplate.from_messages([
    # ('system', 'You are a helpful writer. You get 6 or 7 pieces of data about a person, and write a short introduction'
    #            ' paragraph about them. The introduction length must be 120 to 150 words. At the end of the introduction'
    #            ' there is an email line generated from the users name. Make sure you break lines properly. '
    #            'You will be provided with 2 examples on how the introduction should look and feel.'),
    ('system', "You are a helpful assistant. Write a 120-150 word introduction. Maintain the formating like previous"
               "examples. and add a header line saying 'your introduction'."),
    MessagesPlaceholder(variable_name='history'), # Add this to enable history
    # Example pair 1
    ('human', example_human_text1),
    ('ai', example_AI_text1),
    # Example pair 2
    ('human', example_human_text2),
    ('ai', example_AI_text2),

    ('human', "Full name: {full_name}\n Role or degree: {role}\n Experience: {experience}\n top 3 Skills: {skills}\n"
              "Major achievement: {achievement}\n Goal: {goal}\n Optional fun fact: {fun_fact}\n "
              "Additional question: {question}"),
])

# create the llm object
llm : ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
    model = config[GEMINI_MODEL_NAME],
    api_key = config[GEMINI_API_KEY],
    temperature = config[GEMINI_TEMPERATURE],
)

# create the parser
parser : StrOutputParser = StrOutputParser()

# build chain out of previous components
chain = prompt_template | llm | parser


# Collect data from user by asking them question
print(" ### I will write a short introduction for you. But first, I need to ask you a few questions. ###")
full_name : str = input("1. What is your name? ")
role : str = input("2. What your current role or degree? ")
experience : str = input("3. How many years of experience or seniority do you have? ")
skills : str = input("4. What are your top 3 skills? (please separate them with a comma) ")
achievement : str = input("5. What is one achievement you're proud of? ")
goal : str = input("6. What are you looking for? or what is your goal? ")
fun_fact : str = input("7. What is a fun fact about yourself? (press Enter to skip) ")
print("Please wait while we generate your introduction.\n")

history: list[BaseMessage] = [] # save chat history in list to be sent to llm
question : str = ""

# invoke the chain and pass all collected data to prompt template
introduction: str = chain.invoke({"history" : history, "full_name": full_name, "role": role, "experience": experience,
                                  "skills": skills, "achievement": achievement, "goal": goal, "fun_fact": fun_fact,
                                  "question": question})

# record history of first interaction
history.append(HumanMessage(content=question))
history.append(AIMessage(content=introduction))

# print output of the chain
print(f"{introduction}")


# refinement loop - let user ask the llm to make refinements to the introduction, until they say 'done'
while True:
    question : str = input(" >>>> Would you like to ask a question or request a refinement? (type 'done' if you want to finish) ")
    if question == 'done':
        break
    history.append(HumanMessage(content=question))
    introduction: str = chain.invoke(
        {"history": history, "full_name": full_name, "role": role, "experience": experience,
         "skills": skills, "achievement": achievement, "goal": goal, "fun_fact": fun_fact, "question": question})

    print("please wait while we generate your introduction.\n")
    print("the length of history is:", len(history))
    print(f"{introduction}")
    history.append(AIMessage(content=introduction))

