# Solution to: Assignment 1 — "Ask-then-Introduce" (One-Shot)
import os
from pprint import pprint

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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

# create the template class
prompt_template : ChatPromptTemplate = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful writer. You get 6 or 7 pieces of data about a person, and write a short introduction'
               ' paragraph about them. The introduction length must be 120 to 150 words. At the end of the introduction'
               ' there is an email line generated from the users name. Make sure you break line properly. '),
    ('human', "Full name: {full_name}\n Role or degree: {role}\n Experience: {experience}\n top 3 Skills: {skills}\n"
              "Major achievement: {achievement}\n Goal: {goal}\n Optional fun fact: {fun_fact}"),
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

introduction: str = chain.invoke({"full_name": full_name, "role": role, "experience": experience,
                                  "skills": skills, "achievement": achievement, "goal": goal, "fun_fact": fun_fact})
print(f"=== Your Introduction ===\n\n{introduction}")

# # chat loop (no memory)
# while(True):
#     question : str = input(" >>>> user please ask a question: ")
#     if question == 'exit':
#         break
#     answer : str = chain.invoke({"question" : question})
#
#     print(f"AI: {answer}")

