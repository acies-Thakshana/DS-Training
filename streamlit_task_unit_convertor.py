import streamlit as st
import time

fun_facts = {
    "Length": "Did you know? The Eiffel Tower can shrink by about 6 inches in cold weather!",
    "Weight": "Fun Fact: The tongue of a blue whale can weigh as much as an elephant!",
    "Temperature": "Surprise! The coldest temperature ever recorded on Earth was -128.6°F (-89.2°C) in Antarctica!",
    "Area": "Trivia: The Amazon Rainforest covers an area roughly the size of the entire United States!",
    "Volume": "Did you know? A gallon of honey is heavier than a gallon of water!",
    "Time": "Time fact: Did you know that a day on Venus is longer than a year on Venus?"
}

gif_dict = {
    "Length": r"C:\Users\HP\Desktop\ds_visuals\assests\length.gif",
    "Weight": r"C:\Users\HP\Desktop\ds_visuals\assests\weight.gif",
    "Temperature": r"C:\Users\HP\Desktop\ds_visuals\assests\temperature.gif",
    "Area": r"C:\Users\HP\Desktop\ds_visuals\assests\weight.gif",
    "Volume": "volume.gif",
    "Time": r"assests/time.gif",
    "Same Unit": r"C:\Users\HP\Desktop\ds_visuals\assests\same.gif"
}

def convert_units(category, value, from_unit, to_unit):
    conversions = {
        "Length": {"meters": 1, "feet": 3.28084, "inches": 39.3701, "kilometers": 0.001, "miles": 0.000621371},
        "Weight": {"kilograms": 1, "grams": 1000, "pounds": 2.20462, "ounces": 35.274},
        "Temperature": {"Celsius": lambda x: x, "Fahrenheit": lambda x: (x * 9/5) + 32},
        "Area": {"square meters": 1, "square feet": 10.7639, "acres": 0.000247105},
        "Volume": {"liters": 1, "milliliters": 1000, "gallons": 0.264172},
        "Time": {"seconds": 1, "minutes": 1/60, "hours": 1/3600}
    }
    
    if category == "Temperature":
        return conversions[category][to_unit](value) if from_unit == "Celsius" else (value - 32) * 5/9
    
    return value * (conversions[category][to_unit] / conversions[category][from_unit])

st.markdown("""
    <style>
        .tab-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .tab-button {
            background-color: #f0f0f0;
            color: black;
            border-radius: 8px;
            padding: 12px 20px;
            cursor: pointer;
            border: none;
            font-size: 16px;
            min-width: 120px;
            text-align: center;
        }
        .tab-button:hover {
            background-color: yellow;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Unit Converter⚡</h1>", unsafe_allow_html=True)

time.sleep(0.5)

categories = ["Length", "Weight", "Temperature", "Area", "Volume", "Time"]
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "Length"

def set_category(cat):
    st.session_state["selected_category"] = cat
    st.session_state["from_unit"] = units[cat][0]
    st.session_state["to_unit"] = units[cat][1]
    st.session_state["fun_fact"] = fun_facts[cat]

units = {
    "Length": ["meters", "feet", "inches", "kilometers", "miles"],
    "Weight": ["kilograms", "grams", "pounds", "ounces"],
    "Temperature": ["Celsius", "Fahrenheit"],
    "Area": ["square meters", "square feet", "acres"],
    "Volume": ["liters", "milliliters", "gallons"],
    "Time": ["seconds", "minutes", "hours"]
}

st.markdown('<div class="tab-container">', unsafe_allow_html=True)
cols = st.columns(len(categories))
for i, cat in enumerate(categories):
    with cols[i]:
        if st.button(cat, key=cat):
            set_category(cat)
st.markdown('</div>', unsafe_allow_html=True)

selected_category = st.session_state["selected_category"]
from_unit = st.session_state.get("from_unit", units[selected_category][0])
to_unit = st.session_state.get("to_unit", units[selected_category][1])

st.info(st.session_state.get("fun_fact", "Select a category to see a fun fact!"))

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    from_unit = st.selectbox("From", units[selected_category], index=units[selected_category].index(from_unit), key="from_unit")
with col2:
    to_unit = st.selectbox("To", units[selected_category], index=units[selected_category].index(to_unit), key="to_unit")
with col3:
    value = st.number_input("Enter value", value=0.0, key="input_value")

col4, col5, col6 = st.columns([1, 2, 1])
with col5:
    if st.button("Convert", help="Click to convert the unit"):
        if from_unit == to_unit:
            st.warning("Hey! You're converting the same unit! 🤦‍♂️")
            st.image(gif_dict["Same Unit"], use_container_width=True)
        elif value < 0 and selected_category != "Temperature":
            st.error("Oops! Negative values don't make sense for this conversion! 🚫")
        else:
            result = convert_units(selected_category, value, from_unit, to_unit)
            st.success(f"{value} {from_unit} is {result:.2f} {to_unit}")
            st.image(gif_dict[selected_category], use_container_width=True)