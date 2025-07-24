import tkinter as tk
from tkinter import messagebox
from deep_translator import GoogleTranslator

def translate_text():
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter some text to translate.")
        return
    try:
        translated = GoogleTranslator(source='auto', target='te').translate(input_text)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, translated)
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed:\n{str(e)}")

# GUI
root = tk.Tk()
root.title("Translate to Telugu")
root.geometry("500x400")

tk.Label(root, text="Enter text in any language:").pack(pady=5)
input_box = tk.Text(root, height=6, wrap=tk.WORD)
input_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

tk.Button(root, text="Translate to Telugu", command=translate_text).pack(pady=10)

tk.Label(root, text="Translated to Telugu:").pack(pady=5)
output_box = tk.Text(root, height=6, wrap=tk.WORD, bg="#f0f0f0")
output_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()