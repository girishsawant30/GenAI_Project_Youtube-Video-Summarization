import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os 

from youtube_transcript_api import YouTubeTranscriptApi

#Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a Youtube video summarizer. You will be taking the transcript text 
and summarizing the entire video and providing the important summary in points within 250 words.
Please provide the summary of the text give here."""

#Getting the summary based on Prompt from Google Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

#Getting the transcript data from YT videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1][:11]
        #print(video_id)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en','hi'])

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript

    except Exception as e:
        raise e

## Streamlit App

st.set_page_config(page_title="YT Video Summarizer")
st.header("YouTube Transcript to Detailed Notes Converter")


youtube_link=st.text_input("Enter Youtube Video Link: ")
if youtube_link:
    video_id = youtube_link.split("=")[1][:11]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get detailed notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)


#example - https://www.youtube.com/watch?v=HFfXvfFe9F8&t=52s
# Need to note that the Video ID should be just this part = HFfXvfFe9F8 anything after that will have to be deleted to get the img.