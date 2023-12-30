import spacy
import requests
from bs4 import BeautifulSoup
import re
import spacy

def is_personal_question(question):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(question)

    # Check if the question contains personal pronouns
    personal_pronouns = ["I", "me", "my", "mine", "myself", "you", "your", "yours", "yourself"]
    has_personal_pronoun = any(token.text.lower() in personal_pronouns for token in doc)

    return has_personal_pronoun


#question1 = "What is your favorite color?"
#question2 = "How are you feeling today?"


#is_personal1 = is_personal_question(question1)
#is_personal2 = is_personal_question(question2)

#print(is_personal2)


def web_search(url, query, element_type=None, class_name=None):
    full_url = f"{url}?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from different HTML structures based on element_type and class_name
        if element_type and class_name:
            search_results = soup.find_all(element_type, class_=class_name)
        elif element_type:
            search_results = soup.find_all(element_type)
        else:
            search_results = soup.find_all()

        result_texts = []
        for result in search_results:
            # Extract and print the text content without HTML tags and specified patterns
            result_text = re.sub(r'<[^>]*>', '', result.get_text(strip=True))
            
            # Remove specific patterns
            result_text = result_text.replace("Description", "").replace("Wikipedia", "")

            result_texts.append(result_text.strip())

        # Concatenate the result_texts into a single string
        return ' '.join(result_texts)

    except requests.RequestException as e:
        return f"Error: {str(e)}"



# Example usage
#"what is a good time to eat"
#web_search("https://www.google.com/search", a.lower(), "span", "hgKElc")
#print(str(web_search("https://www.google.com/search", "who is ap dhillon", "div", "PZPZlf hb8SAc")))

#####

"""

THINGS TO ADD TO BACKEND. 

1. shut down the computer
2. sleep the computer
3. raise and lower the volume, brightness
4. open applications
5. open youtube videos
6. remiders, alarms, calendar
7. possibly games
8. remember the user favorite color, food, etc
9. improved dictionary

THINGS TO ADD TO THE FRONTEND.

1. card view of the chat and real time image recognition
2. login
3. cleaner animations using anime.js

"""

#####


#####################################################################################################################################################################################################################################################
#####################################################################################################################################################################################################################################################
