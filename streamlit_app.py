import streamlit as st
import pdfplumber
import pandas as pd
import io

# Title of the Streamlit app
st.title("Anil PDF to Excel Converter")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    st.success("File uploaded successfully!")
    
    # Extract tables from the PDF
    extracted_tables = []
    
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                extracted_tables.append(pd.DataFrame(tables))

    if extracted_tables:
        # Combine all tables into one DataFrame
        df = pd.concat(extracted_tables, ignore_index=True)

        # Show extracted table
        st.write("Extracted Data:")
        st.dataframe(df)

        # Convert DataFrame to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)
        output.seek(0)

        # Download button for Excel file
        st.download_button(
            label="Download Excel File",
            data=output,
            file_name="converted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.error("No tables found in the PDF.")
