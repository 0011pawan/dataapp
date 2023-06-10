from bs4 import BeautifulSoup
import os
import shutil
import tempfile
from xhtml2pdf import pisa
import streamlit as st


def convert_to_pdf(input_file, output_folder_path):
    _, file_extension = os.path.splitext(input_file)
    val = file_extension.lower()

    if val in ['.mhtml', '.html', '.htm', '.igs']:
        with open(input_file, 'rb') as file:
            soup = BeautifulSoup(file, 'html.parser')

        data = soup.find_all()

        output_file_name = os.path.splitext(os.path.basename(input_file))[0] + ".pdf"
        output_file_path = os.path.join(output_folder_path, output_file_name)

        with open(output_file_path, 'wb') as output_file:
            html = "<html><head><meta charset='UTF-8'></head><body>"
            for d in data:
                html += str(d)
            html += "</body></html>"
            pisa.CreatePDF(html, dest=output_file)

        print(f"File converted: {output_file_path}")
        os.remove(input_file)

    elif val == '.pdf':
        output_file_name = os.path.basename(input_file)
        output_file_path = os.path.join(output_folder_path, output_file_name)
        shutil.copyfile(input_file, output_file_path)
        print(f"File copied: {output_file_path}")


def scrape_files(input_folder_path, output_folder_path):
    input_files = [os.path.join(input_folder_path, f) for f in os.listdir(input_folder_path) if os.path.isfile(os.path.join(input_folder_path, f))]

    for input_file in input_files:
        convert_to_pdf(input_file, output_folder_path)


def main():
    st.title("File Conversion App")
    
    input_folder_path = os.path.abspath("C:/Users/hp/Desktop/input")
    output_folder_path = os.path.abspath("C:/Users/hp/Desktop/output23")
    
    if st.button('Scrape Files') and input_folder_path and output_folder_path:
        scrape_files(input_folder_path, output_folder_path)
        st.success('Files scraped successfully!')


if __name__ == '__main__':
    main()
