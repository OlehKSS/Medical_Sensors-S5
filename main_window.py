from tkinter import Frame, Tk, BOTH, Text, Menu, END, Label, Entry, LEFT
from tkinter import filedialog, messagebox
from matplotlib import pyplot, cm
import numpy
from multiprocessing import Process

from _shared.phase_image import PhaseImage
from unroll import unwrap



class S5MainWindow(Frame):

    ftypes = [('Raw data',  '.SUR'), ('All files', '*')]
    title = 'Phase image unwrapping'
    width = 256
    height = 256

    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent
        self.img_wrapped = None
        self.img_unwrapped = None
        self.process_img_wrapped = None
        self.process_img_unwrapped = None        
        self.initUI()

    def initUI(self):

        self.parent.title(S5MainWindow.title)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label="Open", command=self.onOpen)
        filemenu.add_command(label="Unwrap using UNROLL method",\
        command=self.on_local_fitting_unwrap)
        #filemenu.add_command(label="Unwrap with swarn oprimization", command=self.hello)
        filemenu.add_command(label="Save unwrapped phase data", command=self.on_save_phase_data)
        menubar.add_cascade(label="File", menu=filemenu) 

        helpmenu = Menu(menubar, tearoff = 0)
        helpmenu.add_command(label="About...", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.top_frame = Frame(self.parent)
        self.top_frame.pack(side="top", fill="x", expand=False, padx=20, pady=20)

        self.top_left = Frame(self.top_frame)
        self.top_right = Frame(self.top_frame)
        self.top_left.pack(side="left", fill="x", expand=True)
        self.top_right.pack(side="right", fill="x", expand=True)

        Label(self.top_left, text = "Enter Window Size:").pack()
        self.window_size_entry = Entry(self.top_right)
        self.window_size_entry.insert(END, '7')
        self.window_size_entry.pack()  

        # self.txt = Text(self)
        # self.txt.pack(fill=BOTH, expand=1)

    def onOpen(self):

        dlg = filedialog.Open(self, filetypes = S5MainWindow.ftypes)
        file_address = dlg.show()

        if file_address != '':
            #reading binary file
            self.img_wrapped = PhaseImage(256, 256, path = file_address)
            data = self.img_wrapped.read()

            if not (self.process_img_wrapped is None):
                #shut down the process
                    self.process_img_wrapped.terminate()
                    self.process_img_wrapped.join()
            #show image in separate thread
            self.process_img_wrapped = Process(target = self.plot_graph, args = (data,))
            self.process_img_wrapped.start()

            # self.txt.insert(END, text)

    def plot_graph(self, data):
        pyplot.imshow(data, cmap = cm.Greys_r)
        pyplot.show()

    def on_local_fitting_unwrap(self):

        window_size = int(self.window_size_entry.get())
        print("Entered window size is {}".format(window_size))

        if (self.img_wrapped is None):
            messagebox.showerror( "Error", "Open any phase image before running uwrapping.")

        else:
            messagebox.showinfo( "Running", "Press OK to start unwrapping. It might take several minutes. Be patient.") 
            self.img_unwrapped = unwrap(self.img_wrapped, window_size)

            if not (self.process_img_unwrapped is None):
                #shut down the process
                self.process_img_unwrapped.terminate()
                self.process_img_unwrapped.join()
            #show image in separate thread
            self.process_img_unwrapped = Process(target = self.plot_graph,\
            args=(self.img_unwrapped.data,))
            self.process_img_unwrapped.start()

    def on_save_phase_data(self):
        if (self.img_unwrapped is None):
            messagebox.showerror( "Error", "Do not have any unwrapped data to save.")
            return

        file_buffer = filedialog.asksaveasfile(defaultextension=".csv",\
         filetypes = [("Spreadsheet", ".csv")])
        #asksaveasfile return `None` if dialog closed with "cancel".
        if file_buffer is None: 
            return

        numpy.savetxt(file_buffer.name, self.img_unwrapped.phase_data, delimiter=",")
        file_buffer.close()
        messagebox.showinfo( "Operation complete", "You data was saved.")


    def show_about(self):
        messagebox.showinfo( "About", "Simple GUI for displaying phase unwrapping algorithms work")            


def main():

    root = Tk()
    ex = S5MainWindow(root)
    root.geometry("500x500+300+300")
    root.mainloop()  


if __name__ == '__main__':
    main()  