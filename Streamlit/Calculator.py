import streamlit as st
import emoji

# Sidebar - History Section
st.sidebar.markdown("## 📝 History")

# Initialize history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Button to clear history
if st.sidebar.button("🗑 Clear History"):
    st.session_state.history = []

# Display history
for item in st.session_state.history:
    st.sidebar.write(item)

# Dark Mode Toggle
dark_mode = st.toggle("🌗 Toggle Dark Mode")

# Dynamic Text Color Based on Dark Mode
text_color = "white" if dark_mode else "black"

# Apply Dark Mode Styling
if dark_mode:
    st.markdown(
        f"""
        <style>
        body, .stApp {{ background-color: #1E1E1E !important; color: {text_color} !important; }}
        h1, h2, h3, h4, h5, h6, p, label {{ color: {text_color} !important; }}
        .stSidebar {{ background-color: #252525 !important; }}
        .stButton>button {{
            font-size: 35px;
            padding: 15px;
            width: 100%;
            background-color: #333;
            border: 2px solid #555;
            color: white;
        }}
        .stButton>button:hover {{
            background-color: #444;
            border: 2px solid #666;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body, .stApp { background-color: white !important; color: black !important; }
        h1, h2, h3, h4, h5, h6, p, label { color: black !important; }
        .stSidebar { background-color: #F0F0F0 !important; }
        .stButton>button {
            font-size: 35px;
            padding: 15px;
            width: 100%;
            background-color: #f0f0f0;
            border: 2px solid #ccc;
            color: black;
        }
        .stButton>button:hover {
            background-color: #ddd;
            border: 2px solid #bbb;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Page Toggle
page_mode = st.toggle("🔀 Switch Page")

if page_mode:
    st.title("Calculator")

    # Displaying calculator icon
    st.markdown(f"<h1 style='text-align: left;'>{emoji.emojize(':abacus:')}</h1>", unsafe_allow_html=True)

    # Display container with dynamic text color
    display = st.empty()
    display.markdown(f"<div style='font-size: 60px; color: {text_color};'>0</div>", unsafe_allow_html=True)

    # Initialize session variables
    if "input_value" not in st.session_state:
        st.session_state.input_value = ""
    if "operation" not in st.session_state:
        st.session_state.operation = None
    if "stored_value" not in st.session_state:
        st.session_state.stored_value = ""

    # Function to update display
    def update_display(value):
        st.session_state.input_value += value
        display.markdown(f"<div style='font-size: 60px; color: {text_color};'>{st.session_state.input_value}</div>", unsafe_allow_html=True)

    # Function to set operation
    def set_operation(op):
        if st.session_state.input_value:
            st.session_state.operation = op
            st.session_state.stored_value = st.session_state.input_value
            st.session_state.input_value = ""
            display.markdown(f"<div style='font-size: 60px; color: {text_color};'>0</div>", unsafe_allow_html=True)

    # Function to calculate result
    def calculate_result():
        if st.session_state.operation and st.session_state.input_value:
            num1 = float(st.session_state.stored_value)
            num2 = float(st.session_state.input_value)
            result = None
            operation_symbol = ""

            if st.session_state.operation == "Addition":
                result = num1 + num2
                operation_symbol = "+"
            elif st.session_state.operation == "Subtraction":
                result = num1 - num2
                operation_symbol = "-"
            elif st.session_state.operation == "Multiplication":
                result = num1 * num2
                operation_symbol = "×"
            elif st.session_state.operation == "Division":
                if num2 != 0:
                    result = num1 / num2
                    operation_symbol = "÷"
                else:
                    result = "Error (Div by 0)"

            st.session_state.input_value = str(result)
            
            # Update the input display directly with the result (inside the input box)
            display.markdown(f"<div style='font-size: 60px; color: blue;'>{str(result)}</div>", unsafe_allow_html=True)

            # Add the operation history for later reference
            st.session_state.history.append(f"{num1} {operation_symbol} {num2} = {result}")

            # Reset the operation in session state after calculation
            st.session_state.operation = None

    # Function to clear input
    def clear_input():
        st.session_state.input_value = ""
        display.markdown(f"<div style='font-size: 60px; color: {text_color};'>0</div>", unsafe_allow_html=True)

    # Layout - Bigger Buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("7"):
            update_display("7")
        if st.button("4"):
            update_display("4")
        if st.button("1"):
            update_display("1")
        if st.button("0"):
            update_display("0")

    with col2:
        if st.button("8"):
            update_display("8")
        if st.button("5"):
            update_display("5")
        if st.button("2"):
            update_display("2")
        if st.button("."):
            update_display(".")

    with col3:
        if st.button("9"):
            update_display("9")
        if st.button("6"):
            update_display("6")
        if st.button("3"):
            update_display("3")
        if st.button("="):
            calculate_result()
            

    with col4:
        if st.button("➕"):
            set_operation("Addition")
        if st.button("➖"):
            set_operation("Subtraction")
        if st.button("✖"):
            set_operation("Multiplication")
        if st.button("➗"):
            set_operation("Division")
        if st.button("C"):
            clear_input()

    # Button to clear only the main page
    if st.button("🔄 Clear Page"):
        st.session_state.input_value = ""
        st.session_state.operation = None
        st.session_state.stored_value = ""
        st.rerun()

else:
    st.title("Calculator App")
    st.write("---")

    num1 = st.number_input(label="Enter first number", format="%.6f")
    num2 = st.number_input(label="Enter second number", format="%.6f")

    st.write("Operation")

    operations = {
        "➕ Add": "+",
        "➖ Subtract": "-",
        "✖ Multiply": "*",
        "➗ Divide": "/"
    }
    operation = st.radio("Select an operation to perform:", list(operations.keys()))

    if "gif_url" not in st.session_state:
        st.session_state.gif_url = ""
    gif_map = {
    "➕ Add": "images/addition.gif",
    "➖ Subtract": "images/subtraction.gif",
    "✖ Multiply": "images/multiplication.gif",
    "➗ Divide": "images/division.gif"
}

    def calculate():
        """Perform the selected operation"""
        if operation == "➗ Divide" and num2 == 0:
            st.warning("⚠ Division by 0 error. Result is undefined.")
            st.image("images/DivisionError.gif", width=400)
            result = "undefined"  # Set result as a string
        else:
            # Perform the calculation
            result = eval(f"{num1} {operations[operation]} {num2}")

    # Display result
        st.metric(label="Result", value=result)
        st.success(f"Answer = {result}")

        # Store calculation in history
        st.session_state.history.append(f"{num1} {operations[operation]} {num2} = {result}")

        # Update GIF based on the operation
        st.session_state.gif_url = gif_map.get(operation, "")

    if st.button("Calculate result"):
        calculate()
        st.rerun()

    # Display the corresponding GIF if available
    if st.session_state.gif_url:
        st.image(st.session_state.gif_url, use_container_width=True)

    # Button to clear only the main page
    if st.button("🔄 Clear Page"):
        st.toast("Clearing page...")  # Show toast before clearing
        st.session_state.input_value = ""
        st.session_state.operation = None
        st.session_state.stored_value = ""
        st.session_state.gif_url = ""
        st.rerun()
