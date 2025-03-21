import streamlit as st
import os

# Initialize session state for page tracking
if "page" not in st.session_state:
    st.session_state.page = "cover"

# Function to switch pages
def go_to_main():
    st.session_state.page = "main"

# Define GIF file paths (Update these if needed)
joey_gif = r"D:\DS\Streamlit\joey.gif"
pivot_gif = r"D:\DS\Streamlit\giphy.gif"
spiderman_gif = r"D:\DS\Streamlit\spidy.gif"
break_gif = r"D:\DS\Streamlit\we-were-on-a-break.gif"
instructions_gif = r"D:\DS\Streamlit\5c1670e2-b2b3-49b2-8e05-d196b5b505c0_text.gif"
success_gif = r"D:\DS\Streamlit\dunphy.gif"  # Dunphy GIF for success
no_value_gif = r"D:\DS\Streamlit\alex.gif"    # No value GIF

# Cover Page
if st.session_state.page == "cover":
    st.title("🎬 The One Where You Convert Units!")
    # Joey's "How you doin'?" GIF
    if os.path.exists(joey_gif):
        st.image(joey_gif, caption="How you doin'?", use_container_width=True)
    else:
        st.image("https://media.giphy.com/media/9J7tdYltWyXIY/giphy.gif", caption="How you doin'?", use_container_width=True)
    st.write("Easily convert between different units like **Length, Weight, and Temperature** with just a click!")
    if st.button("Continue to Converter"):
        go_to_main()

# Main Unit Converter Page
elif st.session_state.page == "main":
    st.title("Pivoting values between units seamlessly")
    
    # Sidebar Instructions
    with st.sidebar:
        st.header("📌 How to Use")
        if os.path.exists(instructions_gif):
            st.image(instructions_gif, caption="Follow these steps!", use_container_width=True)
        else:
            st.image("https://media.giphy.com/media/l2JehQ2GitHGdVG9y/giphy.gif", caption="Follow these steps!", use_container_width=True)
        st.write("""
        1️⃣ Select a **Conversion Type** (Length, Weight, Temperature).  
        2️⃣ Choose **From Unit** and **To Unit**.  
        3️⃣ Enter a **Value** to convert.  
        4️⃣ Click **Convert** and see the result!  
        5️⃣ Save conversions to history if needed.  
        """)
    
    # Ross's "Pivot!" GIF
    if os.path.exists(pivot_gif):
        st.image(pivot_gif, caption="Pivot! Pivot! Pivot!", use_container_width=True)
    else:
        st.image("https://media.giphy.com/media/J1XGp3xt6TgKk/giphy.gif", caption="Pivot! Pivot! Pivot!", use_container_width=True)
    
    # Conversion factors
    conversion_factors = {
        "Length": {
            "Centimeters": {"Meters": 0.01, "Kilometers": 0.00001, "Centimeters": 1},
            "Meters": {"Centimeters": 100, "Kilometers": 0.001, "Meters": 1},
            "Kilometers": {"Centimeters": 100000, "Meters": 1000, "Kilometers": 1},
        },
        "Weight": {
            "Milligrams": {"Grams": 0.001, "Kilograms": 0.000001, "Milligrams": 1},
            "Grams": {"Milligrams": 1000, "Kilograms": 0.001, "Grams": 1},
            "Kilograms": {"Milligrams": 1000000, "Grams": 1000, "Kilograms": 1},
        },
        "Temperature": {
            "Celsius": {"Fahrenheit": lambda c: (c * 9/5) + 32, "Celsius": lambda c: c},
            "Fahrenheit": {"Celsius": lambda f: (f - 32) * 5/9, "Fahrenheit": lambda f: f},
        }
    }
    
    conversion_type = st.selectbox("Select Conversion Type", list(conversion_factors.keys()))
    from_unit = st.selectbox("From Unit", list(conversion_factors[conversion_type].keys()))
    to_unit = st.selectbox("To Unit", list(conversion_factors[conversion_type][from_unit].keys()))
    
    value = st.number_input("Enter Value", min_value=0.0, format="%f")
    
    if "result" not in st.session_state:
        st.session_state.result = None
    
    # Convert button with all conditions nested inside
    if st.button("Convert"):
        if value == 0.0:
            st.warning("Oops! Please enter a valid number.")
            if os.path.exists(no_value_gif):
                st.image(no_value_gif, caption="You forgot to enter a value!", use_container_width=True)
            else:
                st.image("https://media.giphy.com/media/3og0IL4nUptzI8MMXe/giphy.gif", caption="You forgot to enter a value!", use_container_width=True)
        elif from_unit == to_unit:
            st.error("Error: Please select different units for conversion!")
            if os.path.exists(spiderman_gif):
                st.image(spiderman_gif, caption="Choose different units!", use_container_width=True)
            else:
                st.image("https://media.giphy.com/media/10SvWCbt1ytWCc/giphy.gif", caption="Choose different units!", use_container_width=True)
        else:
            conversion = conversion_factors[conversion_type][from_unit][to_unit]
            if callable(conversion):
                st.session_state.result = conversion(value)
            else:
                st.session_state.result = value * conversion
            st.success(f"Converted Value: {st.session_state.result:.4f} {to_unit}")
            if os.path.exists(success_gif):
                st.image(success_gif, caption="Conversion Successful!", use_container_width=True)
            else:
                st.image("https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif", caption="Conversion Successful!", use_container_width=True)
    
    # Conversion History
    if "history" not in st.session_state:
        st.session_state.history = []
    
    if st.button("Save Conversion"):
        if st.session_state.result is not None:
            st.session_state.history.append(f"{value} {from_unit} = {st.session_state.result:.4f} {to_unit}")
        else:
            st.warning("Please perform a conversion before saving.")
    
    st.subheader("Conversion History")
    if not st.session_state.history:
        if os.path.exists(break_gif):
            st.image(break_gif, caption="We were on a break!", use_container_width=True)
        else:
            st.image("https://media.giphy.com/media/Rzq5WxqNTLtDi/giphy.gif", caption="We were on a break!", use_container_width=True)
        st.write("No conversions yet! Start converting.")
    else:
        for entry in st.session_state.history[-5:]:
            st.write(entry)
