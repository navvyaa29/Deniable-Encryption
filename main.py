import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from database import DatabaseManager

class DeniableEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deniable Encryption Simulator")
        self.root.geometry("800x600")
        
        # Store keys
        self.public_key = None
        self.private_key = None
        
        # Create main sections
        self.create_key_section()
        self.create_sender_section()
        self.create_receiver_section()
        
    def create_key_section(self):
        # Key Generation Section
        key_frame = ttk.Frame(self.root)
        key_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(key_frame, text="SET PUBLIC AND PRIVATE KEYS", font=('Arial', 12, 'bold')).pack()
        ttk.Button(key_frame, text="Generate Keys", command=self.generate_keys).pack(pady=5)
        
    def create_sender_section(self):
        # Sender Section (Blue)
        sender_frame = ttk.Frame(self.root, style='Blue.TFrame')
        sender_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(sender_frame, text="SENDER PHONE", font=('Arial', 11, 'bold')).pack(pady=5)
        
        ttk.Label(sender_frame, text="Enter Real Message:").pack(pady=5)
        self.message_entry = ttk.Entry(sender_frame)
        self.message_entry.pack(pady=5)
        
        ttk.Button(sender_frame, text="Encrypt Message", command=self.encrypt_message).pack(pady=5)
        
        ttk.Label(sender_frame, text="Encrypted Message:").pack(pady=5)
        self.encrypted_text = tk.Text(sender_frame, height=4, width=40)
        self.encrypted_text.pack(pady=5)
        
    def create_receiver_section(self):
        # Receiver Section (Green)
        receiver_frame = ttk.Frame(self.root)
        receiver_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(receiver_frame, text="RECEIVER PHONE", font=('Arial', 11, 'bold')).pack(pady=5)
        
        # User Panel (Yellow)
        user_frame = ttk.LabelFrame(receiver_frame, text="USER PANEL")
        user_frame.pack(fill="both", expand=True, pady=5)
        
        ttk.Label(user_frame, text="Enter Private Key:").pack(pady=5)
        self.private_key_entry = ttk.Entry(user_frame)
        self.private_key_entry.pack(pady=5)
        
        ttk.Button(user_frame, text="Decrypt Message", command=self.decrypt_message).pack(pady=5)
        
        ttk.Label(user_frame, text="Decrypted Message:").pack(pady=5)
        self.decrypted_text = tk.Text(user_frame, height=4, width=40)
        self.decrypted_text.pack(pady=5)
        
        # Hacker Panel (Red)
        hacker_frame = ttk.LabelFrame(receiver_frame, text="HACKER PANEL")
        hacker_frame.pack(fill="both", expand=True, pady=5)
        
        ttk.Label(hacker_frame, text="Enter Wrong Private Key:").pack(pady=5)
        self.wrong_key_entry = ttk.Entry(hacker_frame)
        self.wrong_key_entry.pack(pady=5)
        
        ttk.Button(hacker_frame, text="Decrypt Message (Wrong Key)", 
                  command=self.decrypt_with_wrong_key).pack(pady=5)
        
    def generate_keys(self):
        # Generate a random salt
        salt = b'salt_123'  # In production, use os.urandom(16)
        
        # Generate private key
        self.private_key = ''.join(random.choices(string.digits, k=4))
        
        # Generate public key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.private_key.encode()))
        self.public_key = Fernet(key)
        
        messagebox.showinfo("Success", f"Keys generated successfully!\nPrivate Key: {self.private_key}")
        
    def encrypt_message(self):
        if not self.public_key:
            messagebox.showerror("Error", "Please generate keys first!")
            return
            
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
            
        encrypted_message = self.public_key.encrypt(message.encode())
        self.encrypted_text.delete(1.0, tk.END)
        self.encrypted_text.insert(1.0, encrypted_message.decode())
        
    def decrypt_message(self):
        if not self.private_key:
            messagebox.showerror("Error", "Please generate keys first!")
            return
            
        try:
            entered_key = self.private_key_entry.get()
            encrypted_message = self.encrypted_text.get(1.0, tk.END).strip()
            
            if entered_key == self.private_key:
                # Correct key - perform actual decryption
                decrypted_message = self.public_key.decrypt(encrypted_message.encode())
                self.decrypted_text.delete(1.0, tk.END)
                self.decrypted_text.insert(1.0, decrypted_message.decode())
            else:
                # Wrong key - generate plausible random text
                self.generate_fake_decryption()
                
        except Exception as e:
            self.generate_fake_decryption()
            
    def decrypt_with_wrong_key(self):
        # Always generate plausible random text for hacker panel
        encrypted_message = self.encrypted_text.get(1.0, tk.END).strip()
        fake_text = ''.join(random.choices(
            string.ascii_letters + string.digits, 
            k=len(encrypted_message) // 4
        ))
        messagebox.showinfo("Decryption Result", 
                          f"Decryption failed with wrong key\nGenerated text: {fake_text}")
        
    def generate_fake_decryption(self):
        # Generate plausible-looking random text
        fake_text = ''.join(random.choices(
            string.ascii_letters + string.digits, 
            k=random.randint(5, 15)
        ))
        self.decrypted_text.delete(1.0, tk.END)
        self.decrypted_text.insert(1.0, fake_text)




# Initialize the database
db = DatabaseManager()

# Add some trusted IPs
db.add_ip("192.168.1.100", "Office")
db.add_ip("10.0.0.50", "Home")

# When sending a message, check if IP is trusted
def send_message(recipient_ip, message, encryption_key):
    if db.is_trusted(recipient_ip):
        # Send real encryption key
        return encryption_key
    else:
        # Send fake key or handle untrusted IP
        return generate_fake_key()  # You'll need to implement this
    


    

if __name__ == "__main__":
    root = tk.Tk()
    app = DeniableEncryptionApp(root)
    root.mainloop()