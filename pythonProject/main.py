from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)

def assistant_speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_user_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print("User: ", user_input)
        return user_input.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand your audio.")
        return ""
    except sr.RequestError as e:
        print(f"Error with the speech recognition service; {e}")
        return ""

@app.route('/')
def index():
    assistant_speak("Hello, thanks for calling Dr. Archer’s office. How may I assist you today?")
    return render_template('index.html')

@app.route('/handle_index_selection', methods=['POST'])
def handle_index_selection():
    schedule_option = request.form.get('schedule_option', 'no')

    if schedule_option == 'yes':

        assistant_speak("Sure, just give me a second ,")
        available_time_slots = ["10:00 a.m.", "2:00 p.m.", "4:00 p.m."]
        confirmation_phrases = ["ok", "yes", "sure"]

        return render_template('schedule_appointment.html', available_time_slots=available_time_slots)
    else:
        assistant_speak("No appointment scheduled.")
        return render_template('confirmation.html', confirmation_message="No appointment scheduled.")


@app.route('/confirm_appointment', methods=['POST'])
def confirm_appointment():

    #user_response = request.form['user_response'].lower()
    #available_time_slots = request.form.getlist('available_time_slots')
    user_response = request.form.get('user_response', '10:00 a.m.')

    if user_response == '10:00 a.m.' or user_response == '2:00 p.m.' or user_response == '4:00 p.m.':
        assistant_speak("Okay great! Can I get your phone number and name?")
        return render_template('confirm_appointment.html', user_response=user_response)
    else:
        assistant_speak("Sorry, that time is not available. Please choose another time.")
        return render_template('error.html')

@app.route('/appointment_confirmed', methods=['POST'])
def appointment_confirmed():
    user_name = request.form['user_name']
    phone_number = request.form['phone_number']
    user_response = request.form['user_response']

    confirmation_message = f"Appointment scheduled for {user_response} with {user_name} at {phone_number}."
    assistant_speak(confirmation_message)

    return render_template('appointment_confirmed.html', confirmation_message=confirmation_message)

if __name__ == '__main__':
    app.run(debug=True)

