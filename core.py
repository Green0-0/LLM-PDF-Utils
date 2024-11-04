from libs.model import Model
from libs.process import pdf_to_png
from libs.process import encode_image
import os
from tqdm import tqdm
import time
import math

def transcribe_images(model : Model, images_path : str = "output_images", 
                   rules : list[str] = [
                       "For equations written in LaTeX, write them in the LaTeX form.",
                       "For tables, please write out the table in a readable format.",
                       "For charts and graphs, do not attempt to draw out the chart or graph. Instead, do your best to describe the information the chart and graph shows.",
                       "For images, describe everything in the image in as much detail and specificity as possible.",
                       "For headers, bolding, italics, etc, use markdown."
                   ]) -> str:
    full_transcription = ""
    prompt = "Please transcribe all the text in the image, in the order it should be read (left right, top down). Do not use code blocks for anything that isn't code. Do not attempt to embed images, follow the rules. Do not output anything else, and do not repeat text."
    if len(rules) > 0:
        prompt += " For special elements, please transcribe them with respect to the following rules:\n"
        for i, rule in enumerate(rules, start=1):
            prompt += f"{i}. {rule}\n"    
        prompt.strip()
    images_len = len(os.listdir(images_path))
    print("Beginning transcription of " + str(images_len) + " images")
    for i in tqdm(range(1, images_len + 1)):
        image_path = f"{images_path}/page_{i}.png"
        if os.path.exists(image_path):
            transcription = model.get_completion(prompt, encode_image(image_path), "png")
            full_transcription += transcription
            time.sleep(3) # Prevent ratelimits
    print ("Transcription complete." )
    return full_transcription
    
def tag_text(model : Model, text_path : str = "output_text/full_transcription.txt", batch_lines : int = 100,
             rules : list[str] = [
                 "When there is a new chapter, output a tag before the chapter title saying {{chapter}}",
                 "When there is a new subchapter, output a tag before the subchapter title saying {{subchapter}}",
             ]) -> str:
    with open(text_path, "r") as file:
        text = file.read()
    text_split = text.split("\n")
    prompt = f"-------------\nPlease repeat the text, cleaning up obvious formatting errors and keeping tags like <|begin_image|> the same."
    if len(rules) > 0:
        prompt += " While repeating the text, tag certain elements according to the following rules:\n"
        for i, rule in enumerate(rules, start=1):
            prompt += f"{i}. {rule}\n"    
        prompt.strip()
    end_text = ""
    # do each batch_lines at a time
    print ("Beginning tagging of " + str(len(text_split)) + " text lines, with " + str(math.ceil(len(text_split)/batch_lines)) + " batches.")
    for i in tqdm(range(0, len(text_split), batch_lines)):
        batch = text_split[i:i+batch_lines]
        batch_str = "\n".join(batch)
        tagged_text = model.get_completion(batch_str + "\n" + prompt)
        end_text += tagged_text + "\n"
        print(tagged_text)
        print(end_text)
        time.sleep(3) # Prevent ratelimits
    print ("Tagging complete.")
    return end_text