import streamlit as st
import numpy as np
import random
import time
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="AgriSense", layout="wide")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("⚙️ Settings")

language = st.sidebar.selectbox(
    "🌐 Language",
    [
        "English", "Marathi", "Hindi", "Tamil",
        "Gujarati", "Odia", "Malayalam",
        "Bengali", "Telugu", "Urdu", "Kannada"
    ]
)

view_mode = st.sidebar.radio(
    "📱 View Mode",
    ["Desktop View", "Mobile View"]
)

crop_type = st.sidebar.selectbox(
    "🌾 Select Crop",
    ["Wheat", "Rice", "Cotton", "Soybean", "Sugarcane"]
)

crop_age = st.sidebar.number_input(
    "🌱 Crop Age (Days after sowing)",
    min_value=0,
    max_value=365,
    value=90
)

# --------------------------------------------------
# FULL LANGUAGE ENGINE
# --------------------------------------------------
LANG = {

"English": {
"title":"AgriSense","subtitle":"AI & IoT Based Smart Agriculture Dashboard",
"soil":"Soil Moisture (%)","temp":"Temperature (°C)","humidity":"Humidity (%)",
"irrigation":"Irrigation Status","stress":"Crop Stress Level","harvest":"Harvest Status",
"connectivity":"Sensor Connectivity","weather":"Weather Forecast",
"rain":"Rain Probability (%)","wind":"Wind Speed (km/h)",
"trend":"Soil Moisture Trend (Last 24 Hours)",
"required":"REQUIRED","not_required":"NOT REQUIRED","rain_expected":"NOT REQUIRED (Rain Expected)",
"critical":"CRITICAL","warning":"WARNING","normal":"NORMAL",
"not_ready":"NOT READY","almost_ready":"ALMOST READY","ready":"READY FOR HARVEST",
"connected":"CONNECTED","weak":"WEAK","disconnected":"DISCONNECTED",
"dry":"Dry","moderate":"Moderate","healthy":"Healthy"
},

"Hindi": {
"title":"एग्रीसेंस","subtitle":"एआई आधारित स्मार्ट कृषि डैशबोर्ड",
"soil":"मिट्टी की नमी (%)","temp":"तापमान (°C)","humidity":"आर्द्रता (%)",
"irrigation":"सिंचाई स्थिति","stress":"फसल तनाव स्तर","harvest":"कटाई स्थिति",
"connectivity":"सेंसर कनेक्टिविटी","weather":"मौसम पूर्वानुमान",
"rain":"बारिश संभावना (%)","wind":"हवा की गति (किमी/घंटा)",
"trend":"मिट्टी की नमी रुझान (24 घंटे)",
"required":"आवश्यक","not_required":"आवश्यक नहीं","rain_expected":"आवश्यक नहीं (बारिश संभावित)",
"critical":"गंभीर","warning":"चेतावनी","normal":"सामान्य",
"not_ready":"तैयार नहीं","almost_ready":"लगभग तैयार","ready":"कटाई के लिए तैयार",
"connected":"जुड़ा हुआ","weak":"कमजोर","disconnected":"डिस्कनेक्टेड",
"dry":"सूखा","moderate":"मध्यम","healthy":"स्वस्थ"
},

"Marathi": {
"title":"अ‍ॅग्रीसेन्स","subtitle":"एआय आधारित स्मार्ट शेती डॅशबोर्ड",
"soil":"मातीतील आर्द्रता (%)","temp":"तापमान (°C)","humidity":"आर्द्रता (%)",
"irrigation":"सिंचन स्थिती","stress":"पीक ताण","harvest":"कापणी स्थिती",
"connectivity":"सेन्सर कनेक्टिव्हिटी","weather":"हवामान अंदाज",
"rain":"पावसाची शक्यता (%)","wind":"वाऱ्याचा वेग (किमी/तास)",
"trend":"माती आर्द्रता ट्रेंड (24 तास)",
"required":"आवश्यक","not_required":"आवश्यक नाही","rain_expected":"आवश्यक नाही (पाऊस अपेक्षित)",
"critical":"गंभीर","warning":"इशारा","normal":"सामान्य",
"not_ready":"तयार नाही","almost_ready":"लवकरच तयार","ready":"कापणीसाठी तयार",
"connected":"जोडलेले","weak":"कमकुवत","disconnected":"तुटलेले",
"dry":"कोरडे","moderate":"मध्यम","healthy":"निरोगी"
},

"Tamil": {
"title":"அக்ரிசென்ஸ்","subtitle":"AI அடிப்படையிலான விவசாய டாஷ்போர்டு",
"soil":"மண் ஈரப்பதம் (%)","temp":"வெப்பநிலை (°C)","humidity":"ஈரப்பதம் (%)",
"irrigation":"நீர்ப்பாசன நிலை","stress":"பயிர் அழுத்தம்","harvest":"அறுவடை நிலை",
"connectivity":"சென்சார் இணைப்பு","weather":"வானிலை முன்னறிவு",
"rain":"மழை சாத்தியம் (%)","wind":"காற்று வேகம் (கிமீ/மணி)",
"trend":"மண் ஈரப்பதம் (24 மணி)",
"required":"தேவை","not_required":"தேவை இல்லை","rain_expected":"தேவை இல்லை (மழை எதிர்பார்ப்பு)",
"critical":"அவசரம்","warning":"எச்சரிக்கை","normal":"சாதாரணம்",
"not_ready":"தயார் இல்லை","almost_ready":"கிட்டத்தட்ட தயாராகும்","ready":"அறுவடைக்கு தயாராக உள்ளது",
"connected":"இணைக்கப்பட்டுள்ளது","weak":"பலவீனம்","disconnected":"இணைப்பு இல்லை",
"dry":"உலர்","moderate":"மிதமான","healthy":"ஆரோக்கியமான"
},

"Gujarati": {
"title":"એગ્રીસેન્સ","subtitle":"AI આધારિત ખેતી ડેશબોર્ડ",
"soil":"માટીની ભેજ (%)","temp":"તાપમાન (°C)","humidity":"ભેજ (%)",
"irrigation":"સિંચાઈ સ્થિતિ","stress":"પાક તાણ","harvest":"કાપણી સ્થિતિ",
"connectivity":"સેન્સર કનેક્ટિવિટી","weather":"હવામાન અનુમાન",
"rain":"વરસાદ સંભાવના (%)","wind":"પવન ગતિ (કિમી/કલાક)",
"trend":"માટી ભેજ ટ્રેન્ડ (24 કલાક)",
"required":"આવશ્યક","not_required":"આવશ્યક નથી","rain_expected":"આવશ્યક નથી (વરસાદ શક્ય)",
"critical":"ગંભીર","warning":"ચેતવણી","normal":"સામાન્ય",
"not_ready":"તૈયાર નથી","almost_ready":"લગભગ તૈયાર","ready":"કાપણી માટે તૈયાર",
"connected":"જોડાયેલ","weak":"નબળું","disconnected":"ડિસ્કનેક્ટેડ",
"dry":"સુકું","moderate":"મધ્યમ","healthy":"સ્વસ્થ"
},

"Odia": {
"title":"ଏଗ୍ରିସେନ୍ସ","subtitle":"AI ଆଧାରିତ କୃଷି ଡ୍ୟାଶବୋର୍ଡ",
"soil":"ମାଟି ଆର୍ଦ୍ରତା (%)","temp":"ତାପମାତ୍ରା (°C)","humidity":"ଆର୍ଦ୍ରତା (%)",
"irrigation":"ସିଚାଇ ଅବସ୍ଥା","stress":"ଫସଲ ଚାପ","harvest":"କାଟିବା ଅବସ୍ଥା",
"connectivity":"ସେନ୍ସର ସଂଯୋଗ","weather":"ପାଣିପାଗ ପୂର୍ବାନୁମାନ",
"rain":"ବର୍ଷା ସମ୍ଭାବନା (%)","wind":"ପବନ ଗତି (କିମି/ଘଣ୍ଟା)",
"trend":"ମାଟି ଆର୍ଦ୍ରତା ଟ୍ରେଣ୍ଡ (24 ଘଣ୍ଟା)",
"required":"ଆବଶ୍ୟକ","not_required":"ଆବଶ୍ୟକ ନୁହେଁ","rain_expected":"ଆବଶ୍ୟକ ନୁହେଁ (ବର୍ଷା ସମ୍ଭାବନା)",
"critical":"ଗୁରୁତର","warning":"ଚେତାବନୀ","normal":"ସାଧାରଣ",
"not_ready":"ପ୍ରସ୍ତୁତ ନୁହେଁ","almost_ready":"ପ୍ରାୟ ପ୍ରସ୍ତୁତ","ready":"କାଟିବା ପାଇଁ ପ୍ରସ୍ତୁତ",
"connected":"ସଂଯୁକ୍ତ","weak":"ଦୁର୍ବଳ","disconnected":"ବିଚ୍ଛିନ୍ନ",
"dry":"ଶୁଷ୍କ","moderate":"ମଧ୍ୟମ","healthy":"ସ୍ୱସ୍ଥ"
},

"Malayalam": {
"title":"അഗ്രിസെൻസ്","subtitle":"AI അടിസ്ഥാനമാക്കിയ കാർഷിക ഡാഷ്ബോർഡ്",
"soil":"മണ്ണിലെ ഈർപ്പം (%)","temp":"താപനില (°C)","humidity":"ഈർപ്പം (%)",
"irrigation":"ജലസേചന നില","stress":"വിള സമ്മർദ്ദം","harvest":"വിളവെടുപ്പ് നില",
"connectivity":"സെൻസർ ബന്ധം","weather":"കാലാവസ്ഥ പ്രവചനം",
"rain":"മഴ സാധ്യത (%)","wind":"കാറ്റിന്റെ വേഗം (കിമീ/മണി)",
"trend":"മണ്ണിലെ ഈർപ്പം (24 മണിക്കൂർ)",
"required":"ആവശ്യമാണ്","not_required":"ആവശ്യമില്ല","rain_expected":"ആവശ്യമില്ല (മഴ പ്രതീക്ഷ)",
"critical":"ഗുരുതരം","warning":"മുന്നറിയിപ്പ്","normal":"സാധാരണ",
"not_ready":"തയ്യാറല്ല","almost_ready":"ഏകദേശം തയ്യാറായി","ready":"വിളവെടുപ്പിന് തയ്യാറാണ്",
"connected":"കണക്റ്റഡ്","weak":"ബലഹീന","disconnected":"ഡിസ്കണക്റ്റഡ്",
"dry":"ഉണങ്ങി","moderate":"മിതമായ","healthy":"ആരോഗ്യകരം"
},

"Bengali": {
"title":"এগ্রিসেন্স","subtitle":"AI ভিত্তিক কৃষি ড্যাশবোর্ড",
"soil":"মাটির আর্দ্রতা (%)","temp":"তাপমাত্রা (°C)","humidity":"আর্দ্রতা (%)",
"irrigation":"সেচ অবস্থা","stress":"ফসল চাপ","harvest":"ফসল কাটার অবস্থা",
"connectivity":"সেন্সর সংযোগ","weather":"আবহাওয়ার পূর্বাভাস",
"rain":"বৃষ্টি সম্ভাবনা (%)","wind":"বায়ুর গতি (কিমি/ঘন্টা)",
"trend":"মাটির আর্দ্রতা (২৪ ঘন্টা)",
"required":"প্রয়োজন","not_required":"প্রয়োজন নেই","rain_expected":"প্রয়োজন নেই (বৃষ্টি সম্ভাবনা)",
"critical":"গুরুতর","warning":"সতর্কতা","normal":"স্বাভাবিক",
"not_ready":"প্রস্তুত নয়","almost_ready":"প্রায় প্রস্তুত","ready":"ফসল কাটার জন্য প্রস্তুত",
"connected":"সংযুক্ত","weak":"দুর্বল","disconnected":"বিচ্ছিন্ন",
"dry":"শুকনো","moderate":"মাঝারি","healthy":"সুস্থ"
},

"Telugu": {
"title":"అగ్రిసెన్స్","subtitle":"AI ఆధారిత వ్యవసాయ డాష్‌బోర్డ్",
"soil":"మట్టిలో తేమ (%)","temp":"ఉష్ణోగ్రత (°C)","humidity":"తేమ (%)",
"irrigation":"నీటి స్థితి","stress":"పంట ఒత్తిడి","harvest":"పంట కోత స్థితి",
"connectivity":"సెన్సార్ కనెక్టివిటీ","weather":"వాతావరణ అంచనా",
"rain":"వర్షం అవకాశం (%)","wind":"గాలి వేగం (కిమీ/గం)",
"trend":"మట్టి తేమ (24 గంటలు)",
"required":"అవసరం","not_required":"అవసరం లేదు","rain_expected":"అవసరం లేదు (వర్షం అవకాశం)",
"critical":"తీవ్రమైన","warning":"హెచ్చరిక","normal":"సాధారణం",
"not_ready":"సిద్ధంగా లేదు","almost_ready":"దాదాపు సిద్ధం","ready":"పంట కోతకు సిద్ధం",
"connected":"కనెక్ట్ అయ్యింది","weak":"బలహీన","disconnected":"డిస్కనెక్ట్",
"dry":"ఎండ","moderate":"మధ్యస్థ","healthy":"ఆరోగ్యకరం"
},

"Urdu": {
"title":"ایگری سینس","subtitle":"AI پر مبنی زرعی ڈیش بورڈ",
"soil":"مٹی کی نمی (%)","temp":"درجہ حرارت (°C)","humidity":"نمی (%)",
"irrigation":"آبپاشی کی حالت","stress":"فصل دباؤ","harvest":"کٹائی کی حالت",
"connectivity":"سینسر کنیکٹیویٹی","weather":"موسم کی پیشگوئی",
"rain":"بارش کا امکان (%)","wind":"ہوا کی رفتار (کلومیٹر/گھنٹہ)",
"trend":"مٹی کی نمی (24 گھنٹے)",
"required":"ضروری","not_required":"ضروری نہیں","rain_expected":"ضروری نہیں (بارش متوقع)",
"critical":"سنگین","warning":"انتباہ","normal":"معمول",
"not_ready":"تیار نہیں","almost_ready":"تقریباً تیار","ready":"کٹائی کے لیے تیار",
"connected":"منسلک","weak":"کمزور","disconnected":"منقطع",
"dry":"خشک","moderate":"درمیانہ","healthy":"صحت مند"
},

"Kannada": {
"title":"ಅಗ್ರಿಸೆನ್ಸ್","subtitle":"AI ಆಧಾರಿತ ಕೃಷಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
"soil":"ಮಣ್ಣಿನ ತೇವಾಂಶ (%)","temp":"ತಾಪಮಾನ (°C)","humidity":"ಆದ್ರತೆ (%)",
"irrigation":"ನೀರಾವರಿ ಸ್ಥಿತಿ","stress":"ಬೆಳೆ ಒತ್ತಡ","harvest":"ಕೊಯ್ಲು ಸ್ಥಿತಿ",
"connectivity":"ಸೆನ್ಸರ್ ಸಂಪರ್ಕ","weather":"ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ",
"rain":"ಮಳೆಯ ಸಾಧ್ಯತೆ (%)","wind":"ಗಾಳಿ ವೇಗ (ಕಿಮೀ/ಗಂ)",
"trend":"ಮಣ್ಣಿನ ತೇವಾಂಶ (24 ಗಂಟೆ)",
"required":"ಅವಶ್ಯಕ","not_required":"ಅವಶ್ಯಕವಿಲ್ಲ","rain_expected":"ಅವಶ್ಯಕವಿಲ್ಲ (ಮಳೆ ಸಾಧ್ಯತೆ)",
"critical":"ಗಂಭೀರ","warning":"ಎಚ್ಚರಿಕೆ","normal":"ಸಾಮಾನ್ಯ",
"not_ready":"ಸಿದ್ಧವಾಗಿಲ್ಲ","almost_ready":"ಸಮೀಪದಲ್ಲಿದೆ","ready":"ಕೊಯ್ಲಿಗೆ ಸಿದ್ಧ",
"connected":"ಸಂಪರ್ಕಿತ","weak":"ದೌರ್ಬಲ್ಯ","disconnected":"ಸಂಪರ್ಕ ಇಲ್ಲ",
"dry":"ಒಣ","moderate":"ಮಧ್ಯಮ","healthy":"ಆರೋಗ್ಯಕರ"
}

}

T = LANG[language]

# --------------------------------------------------
# SENSOR SIMULATION
# --------------------------------------------------
soil = np.random.randint(20,80)
temp = np.random.randint(25,40)
humidity = np.random.randint(30,75)
signal_raw = random.choice(["connected","weak","disconnected"])
signal = T[signal_raw]

forecast_temp = np.random.randint(24,38)
rain_probability = np.random.randint(0,100)
wind_speed = np.random.randint(5,25)

# --------------------------------------------------
# AI LOGIC
# --------------------------------------------------
if soil < 35 and rain_probability < 60:
    irrigation_text = T["required"]
elif rain_probability > 60:
    irrigation_text = T["rain_expected"]
else:
    irrigation_text = T["not_required"]

if soil < 30 or temp > 37:
    stress_text = T["critical"]
elif soil < 45 or temp > 33:
    stress_text = T["warning"]
else:
    stress_text = T["normal"]

harvest_days = {"Wheat":120,"Rice":150,"Cotton":180,"Soybean":100,"Sugarcane":300}
target = harvest_days[crop_type]

if crop_age < target*0.6:
    harvest_text = T["not_ready"]
elif crop_age < target*0.9:
    harvest_text = T["almost_ready"]
else:
    harvest_text = T["ready"]

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(f"# 🌾 {T['title']}")
st.caption(T["subtitle"])

# --------------------------------------------------
# METRICS
# --------------------------------------------------
c1,c2,c3 = st.columns(3)
c1.metric(T["soil"], soil)
c2.metric(T["temp"], temp)
c3.metric(T["humidity"], humidity)

st.divider()

c4,c5 = st.columns(2)
c4.metric(T["irrigation"], irrigation_text)
c4.metric(T["stress"], stress_text)
c5.metric(T["harvest"], harvest_text)
c5.metric(T["connectivity"], signal)

# --------------------------------------------------
# WEATHER
# --------------------------------------------------
st.divider()
st.subheader("🌤 "+T["weather"])

w1,w2,w3 = st.columns(3)
w1.metric(T["temp"], forecast_temp)
w2.metric(T["rain"], rain_probability)
w3.metric(T["wind"], wind_speed)



# --------------------------------------------------
# FIELD MAP
# --------------------------------------------------
st.divider()
st.subheader("🗺 Interactive Field Map")

image = Image.open("farm.png")
buffer = BytesIO()
image.save(buffer,format="PNG")
img_str = base64.b64encode(buffer.getvalue()).decode()

fig = go.Figure()
fig.add_layout_image(dict(
    source=f"data:image/png;base64,{img_str}",
    x=0,y=1,sizex=1,sizey=1,
    xref="paper",yref="paper",
    sizing="stretch",layer="below"
))

zone_values = {
"Zone A":np.random.randint(20,80),
"Zone B":np.random.randint(20,80),
"Zone C":np.random.randint(20,80),
"Zone D":np.random.randint(20,80)
}

zones = {"Zone A":(0.25,0.75),"Zone B":(0.75,0.75),
         "Zone C":(0.25,0.25),"Zone D":(0.75,0.25)}

for zone,(x,y) in zones.items():
    val = zone_values[zone]
    if val<35:
        color="red"
    elif val<50:
        color="orange"
    else:
        color="green"
    fig.add_trace(go.Scatter(
        x=[x],y=[y],
        mode="markers+text",
        marker=dict(size=50,color=color),
        text=[zone],
        textposition="top center",
        hovertemplate=f"{zone}<br>{T['soil']}: {val}%"
    ))

fig.update_layout(xaxis=dict(visible=False),
                  yaxis=dict(visible=False),
                  margin=dict(l=0,r=0,t=0,b=0),
                  height=650)

fig.update_xaxes(range=[0,1])
fig.update_yaxes(range=[0,1])

st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# AUTO REFRESH
# --------------------------------------------------
time.sleep(60)

st.rerun()
