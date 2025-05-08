import streamlit as st
from PIL import Image
import os

# Set page config
st.set_page_config(
    page_title="Billing System",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f5f5f5;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
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
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='title'>Billing System</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='option-card'>", unsafe_allow_html=True)
        try:
            img = Image.open("./images/1.png")
            st.image(img, use_column_width=True)
        except FileNotFoundError:
            st.error("Employee image not found")
        if st.button("Employee Login", key="emp"):
            try:
                os.system("streamlit run employee.py")
            except:
                st.error("Employee module not found")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='option-card'>", unsafe_allow_html=True)
        try:
            img = Image.open("./images/2.png")
            st.image(img, use_column_width=True)
        except FileNotFoundError:
            st.error("Admin image not found")
        if st.button("Admin Login", key="admin"):
            try:
                os.system("streamlit run admin.py")
            except:
                st.error("Admin module not found")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
