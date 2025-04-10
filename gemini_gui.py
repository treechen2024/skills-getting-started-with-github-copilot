from google.generativeai import GenerativeModel, configure
import tkinter as tk
from tkinter import filedialog, messagebox

# Replace with your actual API key
API_KEY = "AIzaSyBK8Cukatlb4VjsCqcmoeZhw8Ju-peRTTo"

# Configure the API key
configure(api_key=API_KEY)

# Initialize the model
model = GenerativeModel('gemini-1.5-pro')

def create_right_click_menu(widget):
    menu = tk.Menu(window, tearoff=0)
    menu.add_command(label="複製 (⌘C)", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="貼上 (⌘V)", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_command(label="剪下 (⌘X)", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_separator()
    menu.add_command(label="全選 (⌘A)", command=lambda: widget.tag_add(tk.SEL, "1.0", tk.END))
    return menu

def show_menu(event, menu):
    menu.tk_popup(event.x_root, event.y_root)

def save_result():
    generated_text = result_text.get(1.0, tk.END)
    if not generated_text.strip():
        messagebox.showerror("錯誤", "沒有內容可供儲存！")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="儲存結果"
    )

    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(generated_text)
        messagebox.showinfo("成功", f"結果已儲存至：{save_path}")

def generate_content():
    prompt = prompt_entry.get("1.0", tk.END).strip()  # 修改為從 Text 控件獲取內容
    if not prompt:
        messagebox.showerror("錯誤", "請輸入提示語！")
        return

    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, generated_text)
    except Exception as e:
        messagebox.showerror("錯誤", f"發生錯誤：{e}\n請確認 API 金鑰是否正確，並已安裝所需套件。")

# Create the main window
window = tk.Tk()
window.title("Gemini 內容產生器")

# Prompt input
prompt_label = tk.Label(window, text="輸入提示語：")
prompt_label.pack(pady=5)
prompt_entry = tk.Text(window, height=5, width=50)
prompt_entry.pack(pady=5)

# 添加快捷鍵綁定
def bind_shortcuts(widget):
    widget.bind("<Command-a>", lambda e: (widget.tag_add(tk.SEL, "1.0", tk.END), "break"))
    widget.bind("<Command-c>", lambda e: (widget.event_generate("<<Copy>>"), "break"))
    widget.bind("<Command-v>", lambda e: (widget.event_generate("<<Paste>>"), "break"))
    widget.bind("<Command-x>", lambda e: (widget.event_generate("<<Cut>>"), "break"))

# 創建右鍵選單
prompt_menu = create_right_click_menu(prompt_entry)
prompt_entry.bind("<Button-3>", lambda e: show_menu(e, prompt_menu))
bind_shortcuts(prompt_entry)

# Result display
result_label = tk.Label(window, text="產生結果：")
result_label.pack(pady=5)
result_text = tk.Text(window, height=10, width=60)
result_text.pack(pady=5)

# 為結果文本框添加右鍵選單和快捷鍵
result_menu = create_right_click_menu(result_text)
result_text.bind("<Button-3>", lambda e: show_menu(e, result_menu))
bind_shortcuts(result_text)

# Buttons frame
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

# Generate button
generate_button = tk.Button(button_frame, text="產生內容", command=generate_content)
generate_button.pack(side=tk.LEFT, padx=5)

# Save button
save_button = tk.Button(button_frame, text="儲存為 TXT", command=save_result)
save_button.pack(side=tk.LEFT, padx=5)

# Continue button
continue_button = tk.Button(button_frame, text="繼續", command=lambda: prompt_entry.delete("1.0", tk.END))
continue_button.pack(side=tk.LEFT, padx=5)

# Exit button
exit_button = tk.Button(button_frame, text="結束", command=window.destroy)
exit_button.pack(side=tk.LEFT, padx=5)

# Run the GUI
window.mainloop()