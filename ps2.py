from bs4 import BeautifulSoup
import os
import shutil
import tempfile
from xhtml2pdf import pisa
import streamlit as st


def convert_to_pdf(input_file, output_folder_path):
    _, file_extension = os.path.splitext(input_file.name)
    val = file_extension.lower()

    if val in ['.mhtml', '.html', '.htm', '.igs']:
        with open(input_file.name, 'rb') as file:
            soup = BeautifulSoup(file, 'html.parser')

        data = soup.find_all()

        output_file_name = os.path.splitext(os.path.basename(input_file.name))[0] + ".pdf"
        output_file_path = os.path.join(output_folder_path, output_file_name)

        with open(output_file_path, 'wb') as output_file:
            html = "<html><head><meta charset='UTF-8'></head><body>"
            for d in data:
                html += str(d)
            html += "</body></html>"
            pisa.CreatePDF(html, dest=output_file)

        st.write(f"File converted: {output_file_path}")
        os.remove(input_file.name)

    elif val == '.pdf':
        output_file_name = os.path.basename(input_file.name)
        output_file_path = os.path.join(output_folder_path, output_file_name)
        with open(output_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
        st.write(f"File copied: {output_file_path}")


def scrape_files(input_files, output_folder_path):
    for input_file in input_files:
        convert_to_pdf(input_file, output_folder_path)


def main():
    st.title("File Conversion App")
    
    input_folder_path = st.text_input('Input Folder Path')
    output_folder_path = st.text_input('Output Folder Path')
    
    if st.button('Scrape Files') and input_folder_path and output_folder_path:
        input_files = st.file_uploader("Upload files", type=["mhtml", "html", "htm", "igs"], accept_multiple_files=True)
        scrape_files(input_files, output_folder_path)
        st.success('Files scraped successfully!')


if __name__ == '__main__':
    main()
