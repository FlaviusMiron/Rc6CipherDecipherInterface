"""Interface for coding, decoding and visualising histograms of the messages before and after."""

import tkinter as tk
import customtkinter as ctk
import rc6
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import string

class interface():
    def __init__(self):
        self.root = ctk.CTk()
        self.configure_interface()
        self.set_widgets()
            

    def configure_interface(self):
        self.root.title("Ciphring Interface")
        self.root.geometry("1400x600")
        self.message = ""
        self.key = ""
        self.cyphered_message = ""
        self.used_key=""


    def set_widgets(self):
        self.input_text_label = ctk.CTkLabel(self.root,text="Enter plain text")
        self.input_text_label.place(relwidth=0.2, relheight=0.08, relx=0.01, rely=0.01)

        self.input_text_input_area = ctk.CTkEntry(self.root)
        self.input_text_input_area.place(relwidth=0.2, relheight=0.08, relx=0.22, rely=0.01)

        self.input_key_label = ctk.CTkLabel(self.root,text="Enter key")
        self.input_key_label.place(relwidth=0.2, relheight=0.08, relx=0.01, rely=0.11)

        self.input_key_input_area = ctk.CTkEntry(self.root)
        self.input_key_input_area.place(relwidth=0.2, relheight=0.08, relx=0.22, rely=0.11)

        self.cyphered_text_button = ctk.CTkButton(self.root,text="Cipher plain text",command=self.cyphered_text_button_click_event)
        self.cyphered_text_button.place(relwidth=0.2, relheight=0.08, relx=0.01, rely=0.21)

        self.cyphered_text_label = ctk.CTkLabel(self.root,text="Ciphered text")
        self.cyphered_text_label.place(relwidth=0.2, relheight=0.08, relx=0.22, rely=0.21)

        self.decyphered_text_button = ctk.CTkButton(self.root,text="Decipher text",command=self.decyphered_text_button_click_event)
        self.decyphered_text_button.place(relwidth=0.2, relheight=0.08, relx=0.01, rely=0.31)

        self.decyphered_text_label = ctk.CTkLabel(self.root,text="Deciphered text")
        self.decyphered_text_label.place(relwidth=0.2, relheight=0.08, relx=0.22, rely=0.31)

        self.fig1 = Figure()
        self.a = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master = self.root)
        self.canvas1.get_tk_widget().place(relwidth=0.26, relheight=0.6, relx=0.44, rely=0.01)
        self.canvas1.draw()
        self.a.set_title("Plain text histogram")

        self.fig2 = Figure()
        self.b = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master = self.root)
        self.canvas2.get_tk_widget().place(relwidth=0.26, relheight=0.6, relx=0.71, rely=0.01)
        self.canvas2.draw()
        self.b.set_title("Ciphered message histogram")

 


    def cyphered_text_button_click_event(self):
        CBR = False
        message =  self.input_text_input_area.get()

        if len(message) < 16:
            message = message + (" "*(16-len(message)))
        elif len(message) > 16:
            message = self.breakdown(message)
            CBR = True
        self.message = message

        key = self.input_key_input_area.get()

        if len(key) < 16:
            key = key + (" "*(16-len(key)))
        self.key = key[0:16]

        self.used_key = rc6.generate_key(self.key)
        if CBR:
            self.iv = self.generate_iv()
            previous_block = self.iv
            text=""

            for block in message:
                current_block = block

                current_block = self.xor_blocks(current_block, previous_block)

                encrypted_block = rc6.convert_to_array(rc6.encrypt(current_block, self.used_key))
                
                text+=(encrypted_block)  
                
                previous_block = encrypted_block

            encrypted_message = text
            cbr_message = ""
            for item in message:
                cbr_message+=item
            self.message = cbr_message
            print("Plain texxt:",cbr_message,"with length", len(cbr_message))

        else:
            print(message)
            encrypted_message = rc6.convert_to_array(rc6.encrypt(self.message,self.used_key))
    

        self.cyphered_message = encrypted_message

        file = open("cyphered_message.txt","w", encoding="utf-8")
        file.write(str(self.cyphered_message))

        self.cyphered_text_label.configure(text=encrypted_message)

        self.a.clear()
        self.b.clear()

        self.a.stem(self.get_appearances(self.message))
        self.b.stem(self.get_appearances(encrypted_message))

        self.a.set_title("Plain text histogram")
        self.b.set_title("Cyphered message histogram")

        self.canvas1.draw()
        self.canvas2.draw()

    def get_appearances(self,word):
        return [word.count(chr(i)) for i in range(256)]
    
    def breakdown(self,text):
        result = []
        if (len(text) % 16) != 0:
            text = text + " "*(16 - len(text)%16)

        for i in range(0,len(text),16):
            result.append(text[i:i+16])

        return result
    
    def generate_iv(self):
        characters = string.ascii_letters + string.digits
        block = ''.join(random.choice(characters) for _ in range(16))
        return block
        
    def xor_blocks(self,block1,block2):
        result = ""

        for i in range(16):
            result+= chr(ord(block1[i])^ord(block2[i]))
        
        return result
    
    def decyphered_text_button_click_event(self):
        if len(self.cyphered_message) == 0:
            print("No text to decypher")
        else:
            print("Cyphered message:",self.cyphered_message,"with length",len(self.cyphered_message))


            ciphertext=self.cyphered_message
            if len(ciphertext)> 16:

                decrypted_blocks = []
                previous_block = self.iv  # Reset previous block to IV

                ciphertext = self.breakdown(ciphertext)
                for block in ciphertext:
                    decrypted_block = rc6.convert_to_array(rc6.decrypt(block, self.used_key))
                    
                    # XOR decrypted block with previous block (or IV for the first block)
                    decrypted_block = self.xor_blocks(decrypted_block, previous_block)
                    
                    decrypted_blocks.append(decrypted_block)  # Store the decrypted block
                    
                    previous_block = block  # Update previous block
                dm=""
                for items in decrypted_blocks:
                    dm+=items
                self.decyphered_text_label.configure(text=dm)
                print("Decyphereed message:",dm, "with length",len(dm))
                
            else:
                md=rc6.convert_to_array(rc6.decrypt(self.cyphered_message,self.used_key))
                self.decyphered_text_label.configure(text=md)
                print("Decyphereed message:",md,"with length",len(md))



if __name__ == "__main__":
    app = interface()
    app.root.mainloop()

