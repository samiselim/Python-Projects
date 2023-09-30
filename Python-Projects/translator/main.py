import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import libretranslatepy

def show_custom_message_box(message):
    custom_message_box = tk.Toplevel(app)
    custom_message_box.title("Error")
    custom_message_label = tk.Label(custom_message_box, text=message)
    custom_message_label.pack(padx=20, pady=20)


def Translate_fn():
    try:
        translated = lt.translate(input_text.get("1.0" , tk.END) , languages_code[input_lang.get()] ,  languages_code[output_lang.get()])
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0" , translated)
    except KeyError as e:
       show_custom_message_box("Please Choose Valid Lanuguages ! ")
def Clear_fn():
    input_text.delete("1.0" , tk.END)
    output_text.delete("1.0" , tk.END)

lt = libretranslatepy.LibreTranslateAPI("https://translate.argosopentech.com/")

language_data = lt.languages()
languages_name = [lang['name'] for lang in language_data]
languages_code = {lang['name']:lang['code'] for lang in language_data}

app = tk.Tk()
app.geometry("700x400")
app.title("Translator")
app.config(bg="white")

# input shape 
app_name = tk.Label(app,text="Motargem by Sami Selim", font="arial 15 bold" , bg="white")
app_name.place(x=200 , y=0)

input_label= tk.Label(app,text= "Enter Text" , font="arial 13 bold" , bg="white")
input_label.place(x=85 , y=45)

input_text =tk.Text(app, font="arial 10" ,height=11 , width=30 , bg="#FCD1C7" , pady=5)
input_text.place(x=40 , y=120)

input_lang = ttk.Combobox(app , width=20 , values=languages_name)
input_lang.place(x=60 , y=80)
input_lang.set("Choose Input Language")

# Output shape 

output_label= tk.Label(app,text= "Output" , font="arial 13 bold" , bg="white")
output_label.place(x=460, y=45)

output_text =tk.Text(app, font="arial 10" ,height=11 , width=30 , bg="#FCD1C7" , pady=5)
output_text.place(x=400 , y=120)

output_lang = ttk.Combobox(app , width=20 , values=languages_name)
output_lang.place(x=420 , y=80)
output_lang.set("Choose Output Language")

# btn = ttk.Button(app , width=10 , name="Translate")

btn_translate = tk.Button(app , width=7 , height=1 , text="Translate", bg="gray" , command=Translate_fn)
btn_translate.place(x=288 , y=150)

btn_clear = tk.Button(app , width=8 , height=1 , text="Clear", bg="gray" , font="arial 10 bold" , command=Clear_fn)
btn_clear.place(x=288 , y=190)  # youcan use ' padx= '  to configure padding 

app.mainloop()