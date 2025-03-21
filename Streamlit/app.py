import streamlit as st
import base64

def set_background(local_image_path):
    with open(local_image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.2);  /* Adjust last value (0.2 = 20% white overlay) */
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("math ops.jpg")

st.title("💰 Calculator: Because Money Doesn’t Count Itself!")

st.image("https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif", use_container_width=True)

num1 = st.number_input("Enter first number:")
num2 = st.number_input("Enter second number:")

operation = st.selectbox("Choose an operation:", ["➕ (Addition)", "➖ (Subtraction)", "✖️ (Multiplication)", "➗ (Division)"])

def calculate(n1, n2, op):
    try:
        if op == "➕ (Addition)":
            return n1 + n2, "https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif"
        elif op == "➖ (Subtraction)":
            return n1 - n2, "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif"
        elif op == "✖️ (Multiplication)":
            return n1 * n2, "https://media1.giphy.com/media/l2Je66zG6mAAZxgqI/giphy.gif"
        elif op == "➗ (Division)":
            if n2 == 0:
                return "Whoa there! 😵 You just broke the math rules! No zero division!", "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZGt4eGNqeTNsbnE5NnFsZG05ZjJ3eHE1YThkang5OHZibnc3enRudCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fUY3hmVP1TqPcHDhoZ/giphy.gif"
            return n1 / n2, "https://media3.giphy.com/media/VbnUQpnihPSIgIXuZv/giphy.gif"
    except Exception as e:
        return f"Error: {str(e)}", "https://media.giphy.com/media/l2Je3mrlpP6pW/giphy.gif"

if st.button("Calculate"):
    result, gif_url = calculate(num1, num2, operation)
    
    with st.container():
        st.markdown(
            f"""
            <div style="
                background-color: black;
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                width: fit-content;
                margin: auto;
            ">
                Result: {result}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.image(gif_url,use_container_width=True)

