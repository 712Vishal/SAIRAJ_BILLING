import streamlit as st
import os
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Billing System",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    .title {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .option-card {
        background-color: white;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        margin: 1rem;
        text-align: center;
    }
    .option-card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    .option-img {
        max-width: 100%;
        height: auto;
        margin-bottom: 1rem;
    }
    .columns {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='title'>Billing System</h1>", unsafe_allow_html=True)
    
    # Create two columns for the options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='option-card'>", unsafe_allow_html=True)
        # Load and display employee image
        try:
            emp_img = Image.open("./images/1.png")
            st.image(emp_img, use_column_width=True, caption="Employee Login")
        except FileNotFoundError:
            st.error("Employee image not found")
        
        if st.button("Employee Login", key="emp_btn"):
            try:
                os.system("streamlit run employee.py")
            except:
                st.error("Could not launch employee module")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='option-card'>", unsafe_allow_html=True)
        # Load and display admin image
        try:
            admin_img = Image.open("./images/2.png")
            st.image(admin_img, use_column_width=True, caption="Admin Login")
        except FileNotFoundError:
            st.error("Admin image not found")
        
        if st.button("Admin Login", key="admin_btn"):
            try:
                os.system("streamlit run admin.py")
            except:
                st.error("Could not launch admin module")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
