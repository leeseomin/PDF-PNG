import streamlit as st
import os
import tempfile
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text

# 이미지를 추출하는 함수
def extract_images_from_pdf(pdf_path, images_folder):
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            for img_index, img in enumerate(doc.get_page_images(page_num)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # 이미지 파일 저장
                with open(f"{images_folder}/page{page_num + 1}_img{xref}.png", "wb") as img_file:
                    img_file.write(image_bytes)
        doc.close()
        return True
    except Exception as e:
        st.error(f"An error occurred while extracting images: {e}")
        return False

# 텍스트를 추출하는 함수
def extract_text_from_pdf(pdf_path, output_folder):
    try:
        text = extract_text(pdf_path)
        with open(f"{output_folder}/extracted_text.txt", "w", encoding="utf-8") as text_file:
            text_file.write(text)
        return True
    except Exception as e:
        st.error(f"An error occurred while extracting text: {e}")
        return False

# 메인 함수
def main():
    st.title('PDF Image and Text Extractor')

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        # 업로드된 파일을 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name

        pdf_name = uploaded_file.name.split('.')[0]
        current_dir = os.getcwd()
        output_folder = os.path.join(current_dir, "output", pdf_name)
        images_folder = os.path.join(output_folder, "images")

        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(images_folder, exist_ok=True)

        # 이미지와 텍스트 추출
        if extract_images_from_pdf(pdf_path, images_folder) and extract_text_from_pdf(pdf_path, output_folder):
            st.success(f"Images and text extracted successfully to {output_folder}")
        else:
            st.error("Failed to extract images or text.")

        # 임시 파일 삭제
        os.unlink(pdf_path)

if __name__ == "__main__":
    main()
