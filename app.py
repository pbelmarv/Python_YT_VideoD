from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
# import ttkbootstrap as tkb
# from ttkbootstrap import *
import os
from pytube import YouTube
import threading


def main():
    # Configuración de la ventana
    window = Tk()
    window.geometry("712x550")
    window.resizable(False, False)
    window.title("Descargar videos YouTube con Python")
    # logo = PhotoImage(file="pngwing.com.png")

    # Variables
    URLL = StringVar()
    directorio_actual = StringVar()
    total_size = 0

    dif = 0

    # Funciones
    # Obtenemos el directorio desde donde se inicia la app
    def dire_actual():
        directorio_actual.set(os.getcwd())

    # Descarga del video
    def direc():
        directorio = filedialog.askdirectory()
        if directorio != "":
            os.chdir(directorio)
            directorio_actual.set(os.getcwd())

    # Verificamos la url
    def verif_url():
        try:
            youtubeObject = YouTube(URLL.get())
            # print(youtubeObject.title)
            return youtubeObject
        except:
            messagebox.showwarning("ALGO SALIO MAL", "Video no disponible")
            entrada.delete(0, len(URLL.get()))

    def get(c, v):
        global total_size
        if c == "vid":
            try:
                s = v.streams.filter(
                    file_extension="mp4").get_highest_resolution().resolution
                if int(res.replace("p", "")) > 1080:
                    res = 1080
            except:
                s = v.streams.get_highest_resolution()
        else:
            try:
                s = v.streams.filter(only_audio=True).first()
            except:
                s = v.streams.filter(only_audio=True).first()
        total_size = s.filesize
        return s

    def estado(s):
        boton_dire.config(state=s)
        boton_descarga.config(state=s)
        boton_audio.config(state=s)

    def descargando(co, vid):
        global dif
        youtube = get(co, vid)
        try:
            # youtube.register_on_progress_callback(mycb)
            youtube.download()
            messagebox.showinfo("FIN DE DESCARGA",
                                "Descarga finalizada con éxito")
        except:
            messagebox.showwarning(
                "ERROR", "Se ha producido un error en la descarga")
            prog.step(100)
            entrada.delete(0, len(URLL.get()))
        estado('normal')
        eti.place(x=317, y=180)
        eti_porcent.config(text=" ")
        dif = 0
        total_size = 0

    def mycb(total, recvd, ratio, rate, eta):
        global dif
        porcen = (recvd*100/total_size)
        eti_porcent.config(text=((int(porcen), "%")))
        prog.step(porcen-dif)
        dif = porcen

    def descarga(co):
        vid = verif_url()
        if vid != None:
            eti.place(x=306, y=180)
            estado('disabled')
            t1 = threading.Thread(target=descargando, args=(co, vid))
            t1.start()

    # Obtenemos el directorio actual
    dire_actual()

    # GUI
    # Label(window, image=logo).place(x=0, y=0)
    entrada = Entry(window, font=('Arial', 15, 'bold'),
                    textvariable=URLL, width=30)
    entrada.place(x=196, y=130)
    entrada2 = Entry(window, font=('Arial', 8),
                     textvariable=directorio_actual, width=60)
    entrada2.place(x=185, y=455)
    Label(window, width=12, text="DESTINO").place(x=314, y=432)
    Label(window, font=('Arial', 30, 'bold'), text="Python YT VideoDownloader",
          fg="red", bg="navajo white").place(x=103, y=17)
    boton_dire = Button(window, width=20, text="CAMBIAR DIRECTORIO",
                        bg="pale green", command=direc)
    boton_dire.place(x=287, y=270)
    boton_descarga = Button(window, width=20, text="DESCARGAR VIDEO",
                            bg="pale green", command=lambda: descarga("vid"))
    boton_descarga.place(x=287, y=310)
    Label(window, width=12, text="URL de video",
          bg="navajo white").place(x=316, y=109)
    boton_audio = Button(window, width=20, text="EXTRAER AUDIO",
                         bg="pale green", command=lambda: descarga("aud"))
    boton_audio.place(x=287, y=350)
    eti = Label(window, width=12, text="PROGRESO")
    eti.place(x=317, y=180)
    eti_porcent = Label(window, width=4)
    eti_porcent.place(x=392, y=180)
    prog = progressbar = ttk.Progressbar(window)
    prog.place(x=196, y=200, width=335)
    Label(window, font=('Arial', 12), text="2023 - Pbelmarv").place(x=300, y=520)

    window.mainloop()


if __name__ == '__main__':
    main()
