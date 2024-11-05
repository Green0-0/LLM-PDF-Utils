This is a small collection of python files that let you input a PDF, which is then split into images (one page per image), and each image is converted to text using an LLM. Afterwards, the resulting text file can be captioned for RAG purposes, or used for some other purpose.

# Usage Guide:
1. Replace example.pdf with a pdf of your choice
2. Replace api_key.txt with your API key from the provider of your choice (I used mistral)
3. Go to example_transcribe_pdf.py and replace the URL with the API URL of the provider of choice, and the model you want to call. Run the script.
4. Once #3 finishes, go to example_tag_text.py, replace the URL with the API URL of the provider of choice, and the model you want to call, run this script as well.
5. If you left the filepaths alone, the resulting text should be present in output_text/.

# TODO
- Streamlit UI
- Further processing of tagged text
- Better prompts (the current formatting of the transcribed text is a bit weird)
