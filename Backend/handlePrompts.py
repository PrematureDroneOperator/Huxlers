from google import genai
import json
import re

def extract_json(response):
    # Match both 'json``````json', then everything until the next ```
    match = re.search(r'(?:json)?```([\s\S]+?)```', response)
    if match:
        json_str = match.group(1).strip()
    else:
        json_str = response.strip()
    json_str = json_str[5:-1] if json_str.startswith("json") else json_str
    json_str = json_str + "]" if not json_str.endswith("]") else json_str
    return json_str


def read(prompt):
    newPrompt = f"Write a detailed multi-scene video script based on the following description: {prompt}. Include a clear breakdown of each scene, describing the setting, actions, and transitions between scenes in detail. The response should be structured to guide video creation step-by-step with specific scene information. The response shall be given in a json array format, each scene in one key 'scene' : 1 or 'scene' : 2 depending on which scene it is, and with its description as 'description' : whatever the description is, no furether destructutring from here just the decription (such as setting, actions etc) all in plain text inside the description field itself.Keep it exactly 4 scenes only exact"
    client = genai.Client(api_key="AIzaSyA0PsrWLqQhu7_H_gFm4BtgOjWMg-gw3I8")
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=newPrompt,
        )
    response = response.text
    response_json = extract_json(response)
    # Parse JSON string to Python object
    json_obj = json.loads(response_json)
    return json_obj
