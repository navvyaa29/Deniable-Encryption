import tkinter as tk
from tkinter import messagebox, scrolledtext
from encryption import DeniableEncryption

class DeniableEncryptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Deniable Encryption Simulator")
        master.geometry("800x600")

        # Create encryption instance
        self.encryption = DeniableEncryption()

        # Sender Phone UI
        sender_frame = tk.LabelFrame(master, text="Sender Phone", padx=10, pady=10)
        sender_frame.pack(padx=10, pady=10, fill="x")

        # Message input
        tk.Label(sender_frame, text="Message:").pack()
        self.message_input = tk.Entry(sender_frame, width=50)
        self.message_input.pack(pady=5)

        # Encryption type selection
        self.encryption_var = tk.BooleanVar(value=False)
        tk.Checkbutton(sender_frame, text="Use Deniable Encryption", 
                       variable=self.encryption_var).pack()

        # Encrypt Button
        tk.Button(sender_frame, text="Encrypt", 
                  command=self.encrypt_message).pack(pady=5)

        # Receiver Phone UI
        receiver_frame = tk.LabelFrame(master, text="Receiver Phone", padx=10, pady=10)
        receiver_frame.pack(padx=10, pady=10, fill="x")

        # Encrypted message display
        tk.Label(receiver_frame, text="Encrypted Message:").pack()
        self.encrypted_display = scrolledtext.ScrolledText(
            receiver_frame, height=5, width=50, state='disabled'
        )
        self.encrypted_display.pack(pady=5)

        # Decryption type selection
        self.decryption_var = tk.BooleanVar(value=False)
        tk.Checkbutton(receiver_frame, text="Use Deniable Decryption", 
                       variable=self.decryption_var).pack()

        # Decrypt Button
        tk.Button(receiver_frame, text="Decrypt", 
                  command=self.decrypt_message).pack(pady=5)

        # Decrypted message display
        tk.Label(receiver_frame, text="Decrypted Message:").pack()
        self.decrypted_display = scrolledtext.ScrolledText(
            receiver_frame, height=5, width=50, state='disabled'
        )
        self.decrypted_display.pack(pady=5)

        # Shared encrypted message
        self.current_encrypted_message = None

    def encrypt_message(self):
        message = self.message_input.get()
        if not message:
            messagebox.showwarning("Warning", "Please enter a message")
            return

        # Encrypt with selected method
        encrypted = self.encryption.encrypt(
            message, 
            use_deniable=self.encryption_var.get()
        )

        # Update encrypted message display
        self.encrypted_display.config(state='normal')
        self.encrypted_display.delete(1.0, tk.END)
        self.encrypted_display.insert(tk.END, encrypted)
        self.encrypted_display.config(state='disabled')

        # Store for potential decryption
        self.current_encrypted_message = encrypted

    def decrypt_message(self):
        if not self.current_encrypted_message:
            messagebox.showwarning("Warning", "No message to decrypt")
            return

        # Decrypt with selected method
        decrypted = self.encryption.decrypt(
            self.current_encrypted_message, 
            use_deniable=self.decryption_var.get()
        )

        # Update decrypted message display
        self.decrypted_display.config(state='normal')
        self.decrypted_display.delete(1.0, tk.END)
        self.decrypted_display.insert(tk.END, decrypted)
        self.decrypted_display.config(state='disabled')



if __name__ == "__main__":
    main()