from libs.model import Model
from libs.process import pdf_to_png
from libs.process import crop_images_in_folder
import core
import os

with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
        
model = Model(url = "https://api.mistral.ai/v1/chat/completions", api_key=api_key, model="pixtral-12b-2409")
image_path = "output_images"
output_path = "output_text/full_transcription.txt"

# Wipe the image folder of any files
for f in os.listdir(image_path):
    file_path = os.path.join(image_path, f)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

# Create images
pdf_to_png("example.pdf", image_path)

# Crop out headers in text
crop_images_in_folder(image_path, top=125)

# Transcribe images
transcription = core.transcribe_images(model, image_path)

# Save
with open(output_path, "w") as file:
    file.write(transcription)