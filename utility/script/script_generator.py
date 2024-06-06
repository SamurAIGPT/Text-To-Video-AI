import os
from openai import OpenAI
import json

OPENAI_API_KEY = os.getenv('OPENAI_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
        """You are a seasoned content writer for a YouTube Shorts channel, specializing in facts videos. 
        Your facts shorts are concise, each lasting less than 50 seconds (approximately 140 words). 
        They are incredibly engaging and original. When a user requests a specific type of facts short, you will create it.

        For instance, if the user asks for:
        Weird facts
        You would produce content like this:

        Weird facts you don't know:
        - Bananas are berries, but strawberries aren't.
        - A single cloud can weigh over a million pounds.
        - There's a species of jellyfish that is biologically immortal.
        - Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.
        - The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.
        - Octopuses have three hearts and blue blood.

        You are now tasked with creating the best short script based on the user's requested type of 'facts'.

        Keep it brief, highly interesting, and unique.

        Stictly output the script in a JSON format, and only provide a parsable JSON object with the key 'script'.
        """
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
        content = response.choices[0].message.content
        try:
            script = json.loads(content)["script"]
        except Exception as e:
            json_start_index = content.find('{')
            json_end_index = content.rfind('}')
            content = content[json_start_index+1]
            script = json.loads(content)["script"]
        return script

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
