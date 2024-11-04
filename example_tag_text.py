from libs.model import Model
import core
import re
import json

with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
        
model = Model(url = "https://api.mistral.ai/v1/chat/completions", api_key=api_key, model="mistral-large-latest")
input_path = "output_text/full_transcription.txt"
output_path = "output_text/tagged_text.txt"
output_path_split = "output_text/tagged_text_split.json"

tagged_text = core.tag_text(model, input_path)
with open(output_path, "w") as file:
    file.write(tagged_text)

tagged_text_array = re.split(r'{{chapter}}|{{subchapter}}', tagged_text)
for i in range(len(tagged_text_array)):
    tagged_text_array[i] = {"id":i, "content":tagged_text_array[i].strip()}
    
with open(output_path_split, "w") as file:
    json.dump(tagged_text_array, file)