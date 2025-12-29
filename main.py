import streamlit as st
import pandas as pd
import json
from helper import get_open_ai_response

st.set_page_config(
    page_title="Petition Scanner", page_icon="⚡️", layout="wide")

st.title('Hand-written Petition Scanner')

st.caption(
    'Built by Connor Mitchell')
st.write('This is an AI-powered tool designed to efficiently digitize handwritten petition sheets, transforming them into organized, upload-ready CSVs to streamline data management and optimize volunteer efforts.')

def render_results(response):

    raw_response = response.strip()

    # Remove markdown code fences if present
    if raw_response.startswith("```"):
        raw_response = raw_response.strip("`")
        raw_response = raw_response.replace("json\n", "", 1)

    data = json.loads(raw_response)

    if not data:
        st.warning(
                'Sorry, unable to extract information - please try agin.', icon='🤐')
    else:
        st.markdown(f"""#### Signatures """)
        df = pd.DataFrame(data['signatures'])

        st.dataframe(df)

        csv = df.to_csv().encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="petition_signatures.csv",
            mime="text/csv",
        )
            

        

tab1, tab2 = st.tabs(["🗒 Upload", "📸 Snap"])



with tab1:

    uploaded_file = st.file_uploader(label="Upload the petition form you'd like to scan 📸", label_visibility='visible', accept_multiple_files=False, type=[".jpeg", ".png", ".jpg"])

    if uploaded_file is not None:

        bytes_data = uploaded_file.getvalue()
        response = get_open_ai_response(bytes_data, uploaded_file.type)
        
        render_results(response)

        #st.json(response)

    else:
         
         with st.expander(f'Disclaimer: Accuracy and Verification', expanded=False):

            st.markdown(f"This tool uses AI-powered vision technology to digitize handwritten petition sheets. While we strive for accuracy, please note that the results generated may require cross-checking for completeness and correctness. We recommend verifying data before use to ensure reliability.")

with tab2:

    img_file_buffer = st.camera_input("Point your camera at the petition form 📸", help="Snap")

    if img_file_buffer is not None:

        bytes_data = img_file_buffer.getvalue()
        response = get_open_ai_response(bytes_data, img_file_buffer.type)
        text_spinner_placeholder = st.empty()

        if not (response):
            st.warning(
                'Sorry, unable to process the image - please try again.', icon='🤐')
        else:
            render_results(response)