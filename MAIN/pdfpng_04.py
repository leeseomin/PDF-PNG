import tkinter as tk
from tkinter import filedialog, messagebox
import os
import fitz  # PyMuPDF

class PDFImageExtractorApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('PDF Image and Text Extractor')
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
            pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
            current_dir = os.getcwd()
            output_folder = os.path.join(current_dir, pdf_name)
            images_folder = os.path.join(output_folder, "images")

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            if not os.path.exists(images_folder):
                os.makedirs(images_folder)

            images_extracted = self.extract_images_from_pdf(pdf_file, images_folder)
            text_extracted = self.extract_text_from_pdf(pdf_file, output_folder)

            if images_extracted and text_extracted:
                self.status_label.config(text=f"Images and text extracted to {output_folder}")
            else:
                messagebox.showerror("Error", "Failed to extract images or text. Check the console for details.")
        else:
            self.status_label.config(text="No PDF file selected.")

    def extract_images_from_pdf(self, pdf_path, images_folder):
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                for img in doc.get_page_images(page_num):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5:  # GRAY or RGB
                        pix.save(f"{images_folder}/page{page_num + 1}_img{xref}.png")
                    else:  # CMYK: convert to RGB
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.save(f"{images_folder}/page{page_num + 1}_img{xref}.png")
                        pix1 = None
                    pix = None
            doc.close()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def extract_text_from_pdf(self, pdf_path, output_folder):
        try:
            doc = fitz.open(pdf_path)
            with open(f"{output_folder}/extracted_text.txt", "w", encoding="utf-8") as text_file:
                for page in doc:
                    text = page.get_text()
                    text_file.write(text)
                    text_file.write("\n--- Page Break ---\n\n")
            doc.close()
            return True
        except Exception as e:
            print(f"An error occurred while extracting text: {e}")
            return False

if __name__ == '__main__':
    root = tk.Tk()
    app = PDFImageExtractorApp(master=root)
    app.mainloop()
