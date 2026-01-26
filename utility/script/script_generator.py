import json
from utility.config import get_config


def generate_script(topic):
    config = get_config()
    client = config.get_llm_client()
    model = config.get_llm_model()
    provider = config.get_llm_provider()
    
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

        Stictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the script ..."}
        """
    )
    
    if provider == 'gemini':
        content = _call_gemini(client, topic, prompt)
    else:
        content = _call_openai_groq(client, model, topic, prompt)
    
    try:
        # Remove any common prefix that might be added by LLMs (content:, content =, content=, content: , etc.)
        text = content
        for prefix in ['content:', 'content =', 'content =', 'content: ', 'content=']:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
                break
        
        # Try to find complete JSON object or array
        json_start = text.find('{')
        json_end = text.rfind('}')
        
        if json_start == -1 or json_end == -1:
            raise ValueError("No valid JSON found in response")
        
        script_text = text[json_start:json_end+1]
        script = json.loads(script_text)["script"]
        return script
    except Exception as e:
        print(f"Error: {e}")
        raise
    return script


def _call_openai_groq(client, model, topic, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ]
    )
    return response.choices[0].message.content


def _call_gemini(client, topic, prompt):
    response = client.generate_content(
        contents=[
            {"role": "user", "parts": [{"text": f"{prompt}\n\nTopic: {topic}"}]}
        ],
        generation_config={
            "temperature": 0.7,
            "top_p": 0.8,
            "max_output_tokens": 8192,
        }
    )
    text = response.text
    
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    
    return text.strip()
