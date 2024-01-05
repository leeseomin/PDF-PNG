import tkinter as tk
from tkinter import filedialog, messagebox
import os
import fitz  # PyMuPDF

class PDFImageExtractorApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('PDF Image Extractor')
        self.master.geometry("500x200")

        self.init_ui()

    def init_ui(self):
        load_button = tk.Button(self.master, text='Load PDF', command=self.load_pdf)
        load_button.pack(pady=10)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.pack()

    def load_pdf(self):
        pdf_file = filedialog.askopenfilename(title='Select a PDF file', filetypes=[('PDF files', '*.pdf')])
        if pdf_file:
            # PDF 파일 이름 추출 및 현재 실행 폴더 내에 새 폴더 생성
            pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
            current_dir = os.getcwd()
            output_folder = os.path.join(current_dir, pdf_name)

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            if self.extract_images_from_pdf(pdf_file, output_folder):
                self.status_label.config(text=f"Images extracted to {output_folder}")
            else:
                messagebox.showerror("Error", "Failed to extract images. Check the console for details.")
        else:
            self.status_label.config(text="No PDF file selected.")

    def extract_images_from_pdf(self, pdf_path, output_folder):
        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            return False

        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                for img in doc.get_page_images(page_num):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5:       # this is GRAY or RGB
                        pix.save(f"{output_folder}/page{page_num + 1}_img{xref}.png")
                    else:               # CMYK: convert to RGB first
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.save(f"{output_folder}/page{page_num + 1}_img{xref}.png")
                        pix1 = None
                    pix = None
            doc.close()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

if __name__ == '__main__':
    root = tk.Tk()
    app = PDFImageExtractorApp(master=root)
    app.mainloop()
