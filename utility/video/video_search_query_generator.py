import json
import re
from utility.config import get_config
from utility.utils import log_response, LOG_TYPE_GPT

prompt = """# Instructions

Given the following video script and timed captions, extract three visually concrete and specific keywords for each time segment that can be used to search for background videos. The keywords should be short and capture the main essence of the sentence. They can be synonyms or related terms. If a caption is vague or general, consider the next timed caption for more context. If a keyword is a single word, try to return a two-word keyword that is visually concrete. If a time frame contains two or more important pieces of information, divide it into shorter time frames with one keyword each. Ensure that the time periods are strictly consecutive and cover the entire length of the video. Each keyword should cover between 2-4 seconds. The output should be in JSON format, like this: [[[t1, t2], ["keyword1", "keyword2", "keyword3"]], [[t2, t3], ["keyword4", "keyword5", "keyword6"]], ...]. Please handle all edge cases, such as overlapping time segments, vague or general captions, and single-word keywords.

For example, if the caption is 'The cheetah is the fastest land animal, capable of running at speeds up to 75 mph', the keywords should include 'cheetah running', 'fastest animal', and '75 mph'. Similarly, for 'The Great Wall of China is one of the most iconic landmarks in the world', the keywords should be 'Great Wall of China', 'iconic landmark', and 'China landmark'.

Important Guidelines:

Use only English in your text queries.
Each search string must depict something visual.
The depictions have to be extremely visually concrete, like rainy street, or cat sleeping.
'emotional moment' <= BAD, because it doesn't depict something visually.
'crying child' <= GOOD, because it depicts something visual.
The list must always contain the most relevant and appropriate query searches.
['Car', 'Car driving', 'Car racing', 'Car parked'] <= BAD, because it's 4 strings.
['Fast car'] <= GOOD, because it's 1 string.
['Un chien', 'une voiture rapide', 'une maison rouge'] <= BAD, because the text query is NOT in English.

Note: Your response should be the response only and no extra text or data.
  """

def fix_json(json_str):
    # Replace typographical apostrophes with straight quotes
    json_str = json_str.replace("’", "'")
    # Replace any incorrect quotes (e.g., mixed single and double quotes)
    json_str = json_str.replace("“", "\"").replace("”", "\"").replace("‘", "\"").replace("’", "\"")
    # Add escaping for quotes within the strings
    json_str = json_str.replace('"you didn"t"', '"you didn\'t"')
    return json_str

def getVideoSearchQueriesTimed(script,captions_timed):
    end = captions_timed[-1][0][1]
    try:
        
        out = [[[0,0],""]]
        while out[-1][0][1] != end:
            content = call_OpenAI(script,captions_timed).replace("'",'"')
            try:
                out = json.loads(content)
            except Exception as e:
                print("content: \n", content, "\n\n")
                print(e)
                content = fix_json(content.replace("```json", "").replace("```", ""))
                out = json.loads(content)
        return out
    except Exception as e:
        print("error in response",e)
   
    return None

def call_OpenAI(script,captions_timed):
    config = get_config()
    client = config.get_llm_client()
    model = config.get_llm_model()
    provider = config.get_llm_provider()
    
    user_content = """Script: {}
Timed Captions:{}
""".format(script,"".join(map(str,captions_timed)))
    print("Content", user_content)
    
    if provider == 'gemini':
        response = client.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": f"{prompt}\n\n{user_content}"}]}
            ],
            generation_config={
                "temperature":1.0,
                "top_p": 0.9,
                "max_output_tokens": 8192,
            }
        )
        text = response.text.strip()
    else:
        response = client.chat.completions.create(
            model=model,
            temperature=1,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_content}
            ]
        )
        text = response.choices[0].message.content.strip()
    
    text = re.sub('\s+', ' ', text)
    
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    
    text = text.strip()
    
    try:
        parsed = json.loads(text)
        print("Text", text)
        log_response(LOG_TYPE_GPT,script,text)
        return text
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Original text length: {len(text)}")
        print(f"Original text: {text[:300]}")  # Show first 300 chars
        
        # Try to find complete JSON array/object by looking for patterns
        # Pattern 1: Complete JSON object enclosed in braces
        if '{' in text and '}' in text:
            json_start = text.find('{')
            
            # Find matching closing brace by counting
            brace_count = 0
            json_end = json_start
            for i in range(json_start, len(text)):
                if text[i] == '{':
                    brace_count += 1
                elif text[i] == '}':
                    brace_count -= 1
                if brace_count == 0:
                    json_end = i
                    break
            
            if json_end > json_start:
                try:
                    cleaned_text = text[json_start:json_end+1]
                    parsed = json.loads(cleaned_text)
                    print(f"Cleaned JSON (braces): {cleaned_text[:300]}")
                    log_response(LOG_TYPE_GPT,script,cleaned_text)
                    return cleaned_text
                except json.JSONDecodeError:
                    print("Could not repair JSON with brace matching")
        
        # Pattern 2: Handle incomplete JSON at end by completing it
        if text.endswith(','):
            text = text[:-1] + ']'
        elif text.endswith('], ['):
            text += ']]'
        elif not text.endswith(']') and '], [[' in text:
            text += ']]'
        
        try:
            parsed = json.loads(text)
            print(f"Cleaned JSON (completion): {text[:300]}")
            log_response(LOG_TYPE_GPT,script,text)
            return text
        except json.JSONDecodeError:
            pass
        
        # If all else fails, return a minimal valid JSON structure
        print("Using minimal fallback structure")
        print(f"Returning first {min(300, len(text))} chars of processed text")
        return text[:min(len(text), 300)]

def merge_empty_intervals(segments):
    if segments is None:
        print("No background videos available to merge")
        return None
    
    merged = []
    i = 0
    while i < len(segments):
        interval, url = segments[i]
        if url is None:
            # Find consecutive None intervals
            j = i + 1
            while j < len(segments) and segments[j][1] is None:
                j += 1
            
            # Merge consecutive None intervals with the previous valid URL
            if i > 0:
                prev_interval, prev_url = merged[-1]
                if prev_url is not None and prev_interval[1] == interval[0]:
                    merged[-1] = [[prev_interval[0], segments[j-1][0][1]], prev_url]
                else:
                    merged.append([interval, prev_url])
            else:
                merged.append([interval, None])
            
            i = j
        else:
            merged.append([interval, url])
            i += 1
    
    return merged
