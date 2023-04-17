import tkinter as tk
import tkinter.ttk as ttk
import speech_recognition as sr
import threading

lang_code = ""


def record_audio(recognizer, source):
    global stop_recording

    while not stop_recording:
        try:
            # Usar ajuste automático de ganancia de audio
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            if not stop_recording:
                try:
                    text = recognizer.recognize_google(
                        audio, language=lang_code)
                    text_box.delete("1.0", tk.END)
                    text_box.insert(tk.END, "Has dicho: " + text + "\n")
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    text_box.delete("1.0", tk.END)
                    text_box.insert(
                        tk.END, "Error al conectarse al servicio de reconocimiento de voz de Google: {0}\n".format(e))
        except sr.WaitTimeoutError:
            pass
        except sr.RequestError as e:
            text_box.delete("1.0", tk.END)
            text_box.insert(
                tk.END, "Error al conectarse al dispositivo de audio: {0}\n".format(e))

    # Detener la animación de la barra de progreso
    progress_bar.stop()


def start_recognition():
    global stop_recording, lang_code

    stop_recording = False

    lang = lang_var.get()
    if lang == "1":
        lang_code = "es-ES"
    elif lang == "2":
        lang_code = "en-US"
    else:
        return

    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, "Ahora puedes hablar...\n")

    # Activar la barra de progreso
    progress_bar.start()

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_thread = threading.Thread(target=record_audio, args=(r, source))
        audio_thread.start()


def stop_recognition():
    global stop_recording
    stop_recording = True


root = tk.Tk()
root.title("Auditex")

lang_var = tk.StringVar()

lang_label = tk.Label(root, text="Seleccione el idioma:")
lang_label.pack()

es_button = tk.Radiobutton(root, relief="groove",
                           text="Español", variable=lang_var, value="1")
es_button.pack()

en_button = tk.Radiobutton(root, relief="groove",
                           text="Inglés", variable=lang_var, value="2")
en_button.pack()

start_button = tk.Button(root, background="darkgrey", relief="raised", foreground="black",
                         activebackground="grey", activeforeground="white", text="Iniciar Grabación", command=start_recognition)
start_button.pack()

stop_button = tk.Button(root, background="red", relief="raised", foreground="black", activebackground="darkred",
                        activeforeground="white", text="Detener Grabación", command=stop_recognition, state=tk.DISABLED)
stop_button.pack(side=tk.TOP, padx=5)

# Agregar la barra de progreso
progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack()

text_box = tk.Text(root, background="white", border=5, height=10, width=50)
text_box.pack()

root.mainloop()
