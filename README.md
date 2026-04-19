# BrightWay_Workspace_15_4_2026
First homework from Brightway course


## You will need to make a file named .env and copy this into it:
> GEMINI_API_KEY=your_api_key_placeholder
> 
> GEMINI_MODEL_NAME=gemini-2.5-flash
> 
> GEMINI_TEMPERATURE=0.7
> 
Then provide it with your gemini api key, and keep it secret in there!



## Setup — Virtual Environment & Dependencies
Open a terminal ( powershell ) inside project folder and run these commands in order:

Step 1 — create a virtual environment
> python -m venv venv
 if the above does not work, try:
> py -3.11 -m venv venv

Step 2 — activate the virtual environment
Windows (PowerShell):
> venv\Scripts\Activate.ps1

macOS / Linux:
> source venv/bin/activate
> 
Your terminal prompt should now show (venv) at the start. To deactivate the environment later, run: 'deactivate'

Step 3 — upgrade pip
> python -m pip install --upgrade pip

Step 4 — install dependencies
> pip install -r requirements.txt


# If everything works as intended, your solution1 output should look like this:
```shell
(.venv) PS C:\Users\user1\Desktop\BrightWay\workspace\15_04_2026\Assignments\Assignment Solution> python main.py
 ### I will write a short introduction for you. But first, I need to ask you a few questions. ###
1. What is your name? Mike Wazowski
2. What your current role or degree? engineer
3. How many years of experience or seniority do you have? 7
4. What are your top 3 skills? (please separate them with a comma) Coaching, Fixing doors, Scaring
5. What is one achievement you're proud of? I trained the best worker in our bussiness
6. What are you looking for? or what is your goal? I want to become a comedian
7. What is a fun fact about yourself? (press Enter to skip) I climbed Everest     
Please wait while we generate your introduction.

=== Your Introduction ===

Meet Mike Wazowski, an accomplished engineer bringing seven years of experience to the table. Mike's skill set is remarkably diverse, extending beyond traditional engineering to in
clude strong coaching abilities, a practical knack for fixing doors, and even a unique talent for scaring. He takes immense pride in his major achievement of training the best worker in his business, showcasing his dedication to nurturing talent and driving success.

Despite his professional accomplishments, Mike harbors an ambitious personal goal: to pivot into the world of comedy, where he aims to leverage his distinctive perspective and charisma. Adding another impressive feat to his life story, Mike once conquered Mount Everest, demonstrating an adventurous spirit and formidable determination. He is a multi-talented individual with a inspiring drive for both professional excellence and personal growth.

Email: mike.wazowski@email.com
```
