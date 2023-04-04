# Importing useful libraries
import streamlit as st # For creating a web app
# For speech to text 
import speech_recognition as sr
# For saving the audio and playing it
import pyaudio
import wave 

# Set up the web app layout
st.title("The Rambler")
duration = st.sidebar.slider("Recording duration (seconds)", min_value=1, max_value=10, value=5, step=1)
transcription_text = st.empty()

# Defining the audio recording callback function
def record_audio():
    # Creating a speech recognition object
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Creating a display for recording start
        st.info("Recording...")
        
        # Recording audio based on the duration that we passed
        audio_data = r.record(
            source, 
            duration=duration
            )
        
        # Displaying success when the recording is finished
        st.success("Recording finished.")
        
        # Save the audio file locally to be played latter
        with open("recording.wav", "wb") as f:
            f.write(audio_data.get_wav_data())
        
        # Transcribe the audio using SpeechRecognition library
        try:
            # Transcribing the audio using google
            audio_text = r.recognize_google(audio_data)
            transcription_text.text(audio_text)

            # Displaying it to the user
            st.write(f'This is the transcribed audio:\n',{audio_text})
        
        # Handeling errors
        except sr.UnknownValueError:
            st.error("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Speech Recognition service; {e}")
            
# Create the record,stop and play buttons
record_button = st.button("Record")
stop_button = st.button("Stop")
play_button = st.button("Play")

# When the record button is clicked, start recording audio
if record_button:
    record_audio()

# When the stop button is clicked, stop recording audio
if stop_button:
    st.warning("Recording stopped.")

# When the play button is clicked, play the recording
if play_button:
    # Displaying info for playing the audio
    st.info("Playing the audio")
    chunk = 1024

    # Reading the recording file
    wf = wave.open("recording.wav", 'rb')

    # Saving the recorded audio file in an object
    pa = pyaudio.PyAudio()

    # Opening the audio object
    stream = pa.open(
                format=pa.get_format_from_width(wf.getsampwidth()),  
                channels=wf.getnchannels(),  
                rate=wf.getframerate(),  
                output=True)
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()  
    stream.close()  
    pa.terminate()
    
    # Displaying the end of playing audio
    st.info("Finished playing the audio")

