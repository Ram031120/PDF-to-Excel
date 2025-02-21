import streamlit as st
import pandas as pd
import tabula

def main():
    st.title("PDF to Excel Converter")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Convert PDF to DataFrame
        try:
            df = tabula.read_pdf(uploaded_file)
            st.write("PDF successfully converted to DataFrame:")
            st.write(df.head())

            # Create Excel download link
            excel_file = pd.ExcelWriter('output.xlsx')
            df.to_excel(excel_file, index=False, sheet_name='Sheet1')
            excel_file.save()

            # Provide download link to the Excel file
            st.markdown(get_excel_download_link('output.xlsx', 'Download Excel file'), unsafe_allow_html=True)

        except Exception as e:
            st.write("Error converting PDF:", e)

def get_excel_download_link(file_path, link_text):
    excel_url = open(file_path, 'rb').read()
    b64 = base64.b64encode(excel_url).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_path}">{link_text}</a>'
    return href

if __name__ == "__main__":
    main()
