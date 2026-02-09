import customtkinter as ctk
from tkinter import messagebox
import time
import threading

# ========================
# CẤU HÌNH CHUNG
# ========================
ctk.set_appearance_mode("dark")   # dark / light / system
ctk.set_default_color_theme("blue")  # blue / dark-blue / green

# ========================
# APP CHÍNH
# ========================
class ProApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🚀 Pro App - Giao Diện Xịn")
        self.geometry("800x500")
        self.resizable(False, False)

        # Layout chia 2 cột
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        # ========================
        # SIDEBAR
        # ========================
        self.sidebar = ctk.CTkFrame(self, corner_radius=0, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="🌟 PRO APP",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo.pack(pady=30)

        self.btn_home = ctk.CTkButton(
            self.sidebar,
            text="🏠 Trang chủ",
            command=self.show_home,
            corner_radius=20
        )
        self.btn_home.pack(pady=10, padx=20)

        self.btn_tool = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Công cụ",
            command=self.show_tool,
            corner_radius=20
        )
        self.btn_tool.pack(pady=10, padx=20)

        self.btn_exit = ctk.CTkButton(
            self.sidebar,
            text="❌ Thoát",
            fg_color="red",
            hover_color="#aa0000",
            command=self.quit,
            corner_radius=20
        )
        self.btn_exit.pack(side="bottom", pady=20, padx=20)

        # ========================
        # MAIN FRAME
        # ========================
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.create_home_ui()
        self.update_clock()

    # ========================
    # TRANG CHỦ
    # ========================
    def create_home_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.main_frame,
            text="🎉 Chào mừng bạn!",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title.pack(pady=20)

        self.clock_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=18)
        )
        self.clock_label.pack(pady=10)

        desc = ctk.CTkLabel(
            self.main_frame,
            text="Ứng dụng giao diện hiện đại, màu sắc chuyên nghiệp ✨",
            font=ctk.CTkFont(size=14)
        )
        desc.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self.main_frame, width=400)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.start_btn = ctk.CTkButton(
            self.main_frame,
            text="🚀 Bắt đầu tải",
            command=self.start_loading,
            corner_radius=25,
            height=40
        )
        self.start_btn.pack(pady=10)

    # ========================
    # CÔNG CỤ
    # ========================
    def create_tool_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.main_frame,
            text="⚙️ Công Cụ Tính Tổng",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=20)

        self.entry1 = ctk.CTkEntry(self.main_frame, placeholder_text="Nhập số thứ nhất")
        self.entry1.pack(pady=10)

        self.entry2 = ctk.CTkEntry(self.main_frame, placeholder_text="Nhập số thứ hai")
        self.entry2.pack(pady=10)

        calc_btn = ctk.CTkButton(
            self.main_frame,
            text="🧮 Tính",
            command=self.calculate,
            corner_radius=20
        )
        calc_btn.pack(pady=10)

        self.result_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.result_label.pack(pady=10)

    # ========================
    # CHỨC NĂNG
    # ========================
    def show_home(self):
        self.create_home_ui()

    def show_tool(self):
        self.create_tool_ui()

    def calculate(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            result = num1 + num2
            self.result_label.configure(text=f"Kết quả: {result}")
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

    def start_loading(self):
        threading.Thread(target=self.loading_task).start()

    def loading_task(self):
        for i in range(101):
            time.sleep(0.03)
            self.progress.set(i / 100)

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        if hasattr(self, 'clock_label'):
            self.clock_label.configure(text=f"🕒 {current_time}")
        self.after(1000, self.update_clock)

# ========================
# RUN APP
# ========================
if __name__ == "__main__":
    app = ProApp()
    app.mainloop()
