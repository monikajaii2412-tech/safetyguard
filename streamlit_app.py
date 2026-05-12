import streamlit as st
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Women Safety App", page_icon="🚨")
st.title("🚨 Women Safety App")

# ---------- CONFIG ----------
SENDER_EMAIL = "monikajoshi0023gmail.com"     # replace
APP_PASSWORD = "jxrb itsi hxud sqkg"       # replace (Google App Password)

# ---------- EMAIL ----------
def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    server.quit()

# ---------- FORM ----------
name = st.text_input("Your name")
user_email = st.text_input("Your email")
emergency1 = st.text_input("Emergency email 1")
emergency2 = st.text_input("Emergency email 2")

st.markdown("### 📍 Live Location")
st.info("Tap the button below, allow location, then copy latitude/longitude into fields if they don't auto-fill.")

# Browser geolocation (shows values on page)
location_html = """
<div>
  <button onclick="getLocation()">Get My Live Location</button>
  <p id="loc"></p>
</div>
<script>
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
    document.getElementById("loc").innerHTML = "Geolocation not supported.";
  }
}
function showPosition(position) {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  const map = "https://www.google.com/maps?q=" + lat + "," + lon;
  document.getElementById("loc").innerHTML =
    "Latitude: " + lat + "<br>Longitude: " + lon + "<br>" + map;
}
function showError(error) {
  document.getElementById("loc").innerHTML = "Location permission denied or unavailable.";
}
</script>
"""
components.html(location_html, height=180)

lat = st.text_input("Latitude")
lon = st.text_input("Longitude")

def build_message():
    map_link = f"https://www.google.com/maps?q={lat},{lon}"
    return f"""🚨 EMERGENCY ALERT 🚨

Name: {name}
User Email: {user_email}

Message: Please help me immediately.

Live Location:
{map_link}
"""

def can_send():
    return all([name, user_email, emergency1, lat, lon])

# ---------- SOS BUTTON ----------
st.markdown("### 🚨 Manual SOS")

if st.button("SEND SOS EMAIL"):
    if can_send():
        body = build_message()
        try:
            send_email(emergency1, "🚨 Emergency Alert", body)
            if emergency2.strip():
                send_email(emergency2, "🚨 Emergency Alert", body)
            st.success("Alert sent to emergency contacts.")
            st.write("Map link:", f"https://www.google.com/maps?q={lat},{lon}")
        except Exception as e:
            st.error(f"Email failed: {e}")
    else:
        st.warning("Fill name, user email, emergency email 1, latitude, and longitude.")

# ---------- VOICE HELP ----------
st.markdown("### 🎤 Voice Trigger")
st.write('Tap "Start Voice Detection", then say: HELP')

voice_html = """
<div>
  <button onclick="startRecognition()">Start Voice Detection</button>
  <p id="voice_result"></p>
</div>

<script>
function startRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    document.getElementById("voice_result").innerHTML = "Speech recognition not supported.";
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = function(event) {
    const text = event.results[0][0].transcript.toLowerCase();
    document.getElementById("voice_result").innerHTML = "You said: " + text;

    if (text.includes("help")) {
      alert("HELP detected. Use SEND SOS EMAIL to dispatch alert.");
    }
  };

  recognition.onerror = function() {
    document.getElementById("voice_result").innerHTML = "Could not detect voice.";
  };
}
</script>
"""
components.html(voice_html, height=160)

st.caption("Tip: For the cleanest demo, open on your phone browser and allow microphone + location.")
