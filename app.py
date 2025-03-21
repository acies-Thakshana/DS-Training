import streamlit as st

# Custom CSS to style the elements and center them
st.markdown("""
    <style>
    .title {
        font-size: 48px;
        font-weight: bold;
        color: #1E90FF;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .container {
        padding: 20px;
        background-color: #F0F8FF;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .gif-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .result {
        font-size: 28px;
        font-weight: bold;
        color: #32CD32;
        text-align: center;
        background-color: #f7f7f7;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
        font-family: 'Arial', sans-serif;
    }
    .button-center {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .convert-button {
        font-size: 28px;
        background-color: #4CAF50;
        color: white;
        padding: 20px 50px;
        border-radius: 15px;
        border: none;
        cursor: pointer;
    }
    .convert-button:hover {
        background-color: #45a049;
    }
    .input-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .input-field {
        padding: 10px;
        font-size: 16px;
        width: 200px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .dropdown {
        width: 200px;
        font-size: 16px;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# Conversion functions
def convert_length(value, from_unit, to_unit):
    # Conversion factors for length
    length_units = {
        "meters": 1,
        "feet": 3.28084,
        "kilometers": 0.001,
        "miles": 0.000621371
    }
    value_in_meters = value * length_units[from_unit]  # Convert value to meters first
    return value_in_meters / length_units[to_unit]  # Convert from meters to the desired unit

def convert_weight(value, from_unit, to_unit):
    # Conversion factors for weight
    weight_units = {
        "kilograms": 1,
        "grams": 1000,
        "pounds": 2.20462,
        "ounces": 35.274
    }
    value_in_kg = value * weight_units[from_unit]  # Convert value to kilograms first
    return value_in_kg / weight_units[to_unit]  # Convert from kilograms to the desired unit

def convert_temperature(value, from_unit, to_unit):
    # Temperature conversion
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
        else:
            return value  # If both are Celsius, return value
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        else:
            return value  # If both are Fahrenheit, return value
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
        else:
            return value  # If both are Kelvin, return value

# Success gif URL
success_gif = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG05ZWUwbnlud29rdjVhMmlmY3VnMmRleDZ5MGZ3dXpoOGhhdmh2MCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Q81NcsY6YxK7jxnr4v/giphy.gif"

# Title of the app
st.markdown('<div class="title">✨ Unit Converter ✨</div>', unsafe_allow_html=True)

if 'convert_clicked' not in st.session_state:
    st.session_state.convert_clicked = False

# Sidebar for conversion type selection
conversion_type = st.sidebar.selectbox("Select Conversion Type", ["Length", "Weight", "Temperature"])

# Enter Conversion Details section
with st.expander("Enter Conversion Details", expanded=True):
    if conversion_type == "Length":
        from_unit = st.selectbox("From Unit", ["meters", "feet", "kilometers", "miles"], key="from_unit")
        to_unit = st.selectbox("To Unit", ["meters", "feet", "kilometers", "miles"], key="to_unit")
        value = st.text_input(f"Enter value in {from_unit}", key="value")
    elif conversion_type == "Weight":
        from_unit = st.selectbox("From Unit", ["kilograms", "grams", "pounds", "ounces"], key="from_unit")
        to_unit = st.selectbox("To Unit", ["kilograms", "grams", "pounds", "ounces"], key="to_unit")
        value = st.text_input(f"Enter value in {from_unit}", key="value")
    elif conversion_type == "Temperature":
        from_unit = st.selectbox("From Unit", ["Celsius", "Fahrenheit", "Kelvin"], key="from_unit")
        to_unit = st.selectbox("To Unit", ["Celsius", "Fahrenheit", "Kelvin"], key="to_unit")
        value = st.text_input(f"Enter value in {from_unit}", key="value")

# Centering the Convert Button and Result Box
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])  # Add extra space on the sides
    with col1:
        pass  # Empty column to center the button

    with col2:
        if st.button("Convert", key="convert", use_container_width=True, help="Click to convert the entered value"):
            st.session_state.convert_clicked = True

            # Validate input and show the result
            try:
                value = float(value)
                if from_unit == to_unit:
                    st.markdown("<div class='result'>No conversion needed. 😞 Both units are the same!</div>", unsafe_allow_html=True)
                else:
                    if from_unit in ["meters", "feet", "kilometers", "miles"]:
                        result = convert_length(value, from_unit, to_unit)
                        st.markdown(f"<div class='result'>{value} {from_unit} is equal to {result} {to_unit}</div>", unsafe_allow_html=True)
                    elif from_unit in ["kilograms", "grams", "pounds", "ounces"]:
                        result = convert_weight(value, from_unit, to_unit)
                        st.markdown(f"<div class='result'>{value} {from_unit} is equal to {result} {to_unit}</div>", unsafe_allow_html=True)
                    elif from_unit in ["Celsius", "Fahrenheit", "Kelvin"]:
                        result = convert_temperature(value, from_unit, to_unit)
                        st.markdown(f"<div class='result'>{value}° {from_unit} is equal to {result}° {to_unit}</div>", unsafe_allow_html=True)

                    # Show the success GIF after a successful conversion
                    st.markdown("<div class='gif-container'>", unsafe_allow_html=True)
                    st.image(success_gif,  width=200)
                    st.markdown("</div>", unsafe_allow_html=True)

            except ValueError:
                st.markdown("<div class='result'>🚨 Please enter a valid number!</div>", unsafe_allow_html=True)
