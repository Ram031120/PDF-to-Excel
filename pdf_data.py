import pdfplumber
import pandas as pd
import streamlit as st

def extract_pdf_data(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        data = []
        for page in pdf.pages:
            data.append(page.extract_table())  # Extract table data
        
        # Flatten the list and remove empty elements
        table_data = [row for table in data if table for row in table]
        
        df = pd.DataFrame(table_data)
    return df

def main():
    st.title("PDF to Excel Converter")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        df = extract_pdf_data(uploaded_file)
        st.write(df)
        df.to_csv("output.csv", index=False)  # Save to CSV

if __name__ == "__main__":
    main()
