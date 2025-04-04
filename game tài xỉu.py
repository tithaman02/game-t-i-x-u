import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os
import time

class TaiXiuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Trò Chơi Tài Xỉu")
        self.root.geometry("700x550")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)
        
        # Tiền của người chơi
        self.money = 10000
        
        # Kết quả xúc xắc
        self.dice_values = [1, 1, 1]
        
        # Tạo thư mục cho hình ảnh nếu chưa tồn tại
        if not os.path.exists("dice_images"):
            os.makedirs("dice_images")
            self.create_dice_images()
        
        self.setup_ui()
    
    def create_dice_images(self):
        # Hàm này tạo hình ảnh xúc xắc nếu chưa có
        # Tạo hình ảnh đơn giản cho các mặt xúc xắc
        for i in range(1, 7):
            img = Image.new('RGB', (100, 100), color='white')
            dots = []
            
            # Vị trí các chấm dựa trên giá trị xúc xắc
            if i == 1:
                dots = [(50, 50)]
            elif i == 2:
                dots = [(30, 30), (70, 70)]
            elif i == 3:
                dots = [(30, 30), (50, 50), (70, 70)]
            elif i == 4:
                dots = [(30, 30), (30, 70), (70, 30), (70, 70)]
            elif i == 5:
                dots = [(30, 30), (30, 70), (50, 50), (70, 30), (70, 70)]
            elif i == 6:
                dots = [(30, 30), (30, 50), (30, 70), (70, 30), (70, 50), (70, 70)]
            
            # Vẽ các chấm
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            for dot in dots:
                x, y = dot
                draw.ellipse((x-10, y-10, x+10, y+10), fill='black')
            
            # Vẽ viền
            draw.rectangle([(0, 0), (99, 99)], outline='black', width=2)
            
            # Lưu hình ảnh
            img.save(f"dice_images/dice_{i}.png")
    
    def setup_ui(self):
        # Tiêu đề
        self.title_label = tk.Label(
            self.root,
            text="TRÒ CHƠI TÀI XỈU",
            font=("Arial", 24, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        )
        self.title_label.pack(pady=20)
        
        # Khung hiển thị xúc xắc
        self.dice_frame = tk.Frame(self.root, bg="#16213e", padx=20, pady=20)
        self.dice_frame.pack(pady=10)
        
        # Tải hình ảnh xúc xắc
        self.dice_images = []
        for i in range(1, 7):
            img = Image.open(f"dice_images/dice_{i}.png")
            img = ImageTk.PhotoImage(img)
            self.dice_images.append(img)
        
        # Hiển thị 3 xúc xắc
        self.dice_labels = []
        for i in range(3):
            label = tk.Label(self.dice_frame, image=self.dice_images[0], bg="#16213e")
            label.grid(row=0, column=i, padx=10)
            self.dice_labels.append(label)
        
        # Kết quả
        self.result_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.result_frame.pack(pady=10)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="Tổng: 3",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="white"
        )
        self.result_label.grid(row=0, column=0, padx=20)
        
        self.tai_xiu_label = tk.Label(
            self.result_frame,
            text="(XỈU)",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="#4ecca3"
        )
        self.tai_xiu_label.grid(row=0, column=1, padx=20)
        
        # Số tiền
        self.money_label = tk.Label(
            self.root,
            text=f"Số tiền: {self.money:,} VNĐ",
            font=("Arial", 14),
            bg="#1a1a2e",
            fg="white"
        )
        self.money_label.pack(pady=10)
        
        # Đặt cược
        self.bet_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.bet_frame.pack(pady=10)
        
        self.bet_label = tk.Label(
            self.bet_frame,
            text="Số tiền cược:",
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="white"
        )
        self.bet_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.bet_entry = tk.Entry(
            self.bet_frame,
            font=("Arial", 12),
            width=12
        )
        self.bet_entry.grid(row=0, column=1, padx=10, pady=10)
        self.bet_entry.insert(0, "1000")
        
        # Lựa chọn Tài/Xỉu
        self.choice_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.choice_frame.pack(pady=10)
        
        self.tai_button = tk.Button(
            self.choice_frame,
            text="TÀI (11-17)",
            font=("Arial", 12, "bold"),
            bg="#e94560",
            fg="white",
            width=15,
            height=2,
            command=lambda: self.play("TÀI")
        )
        self.tai_button.grid(row=0, column=0, padx=20)
        
        self.xiu_button = tk.Button(
            self.choice_frame,
            text="XỈU (4-10)",
            font=("Arial", 12, "bold"),
            bg="#4ecca3",
            fg="white",
            width=15,
            height=2,
            command=lambda: self.play("XỈU")
        )
        self.xiu_button.grid(row=0, column=1, padx=20)
        
        # Thông tin luật chơi
        self.info_label = tk.Label(
            self.root,
            text="Luật chơi: Tài (11-17), Xỉu (4-10), Ba đồng nhất (Nhà cái thắng)",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#cccccc"
        )
        self.info_label.pack(pady=10)
    
    def roll_dice(self):
        # Hiệu ứng đổ xúc xắc
        for _ in range(10):
            temp_values = [random.randint(1, 6) for _ in range(3)]
            for i in range(3):
                self.dice_labels[i].configure(image=self.dice_images[temp_values[i]-1])
            self.root.update()
            time.sleep(0.1)
        
        # Kết quả cuối cùng
        self.dice_values = [random.randint(1, 6) for _ in range(3)]
        for i in range(3):
            self.dice_labels[i].configure(image=self.dice_images[self.dice_values[i]-1])
        
        # Tính tổng và xác định Tài/Xỉu
        total = sum(self.dice_values)
        self.result_label.config(text=f"Tổng: {total}")
        
        # Kiểm tra ba đồng nhất
        if self.dice_values[0] == self.dice_values[1] == self.dice_values[2]:
            result_text = "BA ĐỒNG NHẤT"
            color = "#ff9a00"
        elif total >= 11:
            result_text = "(TÀI)"
            color = "#e94560"
        else:  # total <= 10
            result_text = "(XỈU)"
            color = "#4ecca3"
        
        self.tai_xiu_label.config(text=result_text, fg=color)
        return total, result_text
    
    def play(self, choice):
        try:
            bet_amount = int(self.bet_entry.get())
            if bet_amount <= 0:
                messagebox.showwarning("Cảnh báo", "Số tiền cược phải lớn hơn 0!")
                return
            
            if bet_amount > self.money:
                messagebox.showwarning("Cảnh báo", "Số tiền cược lớn hơn số tiền bạn có!")
                return
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập số tiền cược hợp lệ!")
            return
        
        # Vô hiệu hóa nút trong khi đổ xúc xắc
        self.tai_button.config(state=tk.DISABLED)
        self.xiu_button.config(state=tk.DISABLED)
        
        # Đổ xúc xắc và nhận kết quả
        total, result_text = self.roll_dice()
        
        # Kiểm tra ba đồng nhất (nhà cái thắng)
        if result_text == "BA ĐỒNG NHẤT":
            self.money -= bet_amount
            message = f"Ba đồng nhất! Nhà cái thắng, bạn thua {bet_amount:,} VNĐ."
        # Kiểm tra Tài
        elif choice == "TÀI" and result_text == "(TÀI)":
            self.money += bet_amount
            message = f"Chúc mừng! Bạn thắng {bet_amount:,} VNĐ."
        # Kiểm tra Xỉu
        elif choice == "XỈU" and result_text == "(XỈU)":
            self.money += bet_amount
            message = f"Chúc mừng! Bạn thắng {bet_amount:,} VNĐ."
        # Thua
        else:
            self.money -= bet_amount
            message = f"Rất tiếc! Bạn thua {bet_amount:,} VNĐ."
        
        # Cập nhật số tiền
        self.money_label.config(text=f"Số tiền: {self.money:,} VNĐ")
        
        # Hiển thị thông báo
        messagebox.showinfo("Kết quả", message)
        
        # Kiểm tra nếu người chơi hết tiền
        if self.money <= 0:
            messagebox.showinfo("Game Over", "Bạn đã hết tiền! Trò chơi kết thúc.")
            self.reset_game()
        
        # Kích hoạt lại nút
        self.tai_button.config(state=tk.NORMAL)
        self.xiu_button.config(state=tk.NORMAL)
    
    def reset_game(self):
        self.money = 10000
        self.money_label.config(text=f"Số tiền: {self.money:,} VNĐ")
        self.bet_entry.delete(0, tk.END)
        self.bet_entry.insert(0, "1000")
        
        # Đặt lại xúc xắc
        self.dice_values = [1, 1, 1]
        for i in range(3):
            self.dice_labels[i].configure(image=self.dice_images[0])
        
        self.result_label.config(text="Tổng: 3")
        self.tai_xiu_label.config(text="(XỈU)", fg="#4ecca3")

if __name__ == "__main__":
    root = tk.Tk()
    game = TaiXiuGame(root)
    root.mainloop()