import streamlit as st
import os

# Set up page layout
st.set_page_config(page_title="Epic Calculator", layout="wide")

st.sidebar.markdown("### 🎭 Open the Calculator")
show_calc = st.sidebar.checkbox("📂 Open Calculator")

if show_calc:
    st.markdown("## 🎉 DUDE! Use a Real Calculator!")

    col1, col2 = st.columns([2, 1]) 

    with col1:
        num1 = st.number_input("Enter first number", value=None, key="num1")
        num2 = st.number_input("Enter second number", value=None, key="num2")

        operation = st.radio("Choose an operation:", ["➕ Add", "➖ Subtract", "✖ Multiply", "➗ Divide"])

        if num1 is not None and num2 is not None:
            def calculate(n1, n2, op):
                if "Add" in op:
                    return n1 + n2
                elif "Subtract" in op:
                    return n1 - n2
                elif "Multiply" in op:
                    return n1 * n2
                elif "Divide" in op:
                    return "error" if n2 == 0 else n1 / n2

            result = calculate(num1, num2, operation)
            st.success(f"✅ **Result: {result}**" if result != "error" else "❌ **Math error!**")

            # GIF Display in Right Column (Only shows after input)
            with col2:
                if result == "error":
                    st.error("Oops! You just broke math! 😵")
                    if os.path.exists("memes-wrong-number.gif"):
                        st.image("memes-wrong-number.gif", use_container_width=True)

                elif (num1 < 10 and num2 < 10):
                    st.info("Father who spent lakhs for your education...XD")
                    if os.path.exists("rajni-darbar.gif"):
                        st.image("rajni-darbar.gif", use_container_width=True)

                elif (("Multiply" in operation or "Divide" in operation) and num1 >= 50_000 and num2 >= 50_000):
                    st.warning("🕶️ NEO!!!!The Matrix is real! 🕶️")
                    if os.path.exists("neo-the-matrix.gif"):
                        st.image("neo-the-matrix.gif", use_container_width=True)

                elif isinstance(result, (int, float)) and result > 1_000_000:
                    st.info("That’s a MASSIVE number!Why don't you open a real CALC!!! 💥")
                    if os.path.exists("boom-mind-blown.gif"):
                        st.image("boom-mind-blown.gif", use_container_width=True)

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #0F0F0F;
            border-right: 4px solid #00FF00;
            color: #00FF00;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #00FF00;
        }
    </style>
""", unsafe_allow_html=True)
