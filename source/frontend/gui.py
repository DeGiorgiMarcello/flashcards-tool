from tkinter import Label, Tk, Button, Entry, messagebox, Checkbutton, BooleanVar, font, Frame
from typing import Dict

from source.backend.card import Card
from source.backend.db import Session
from functools import partial

LABEL_DICT = {
    0: "Front text",
    1: "Front sub text",
    2: "Back text",
    3: "Back subtext",
    4: "Tag",
    5: "Both sides",
}

ATTR_DICT = {
    LABEL_DICT[0]: "front_text",
    LABEL_DICT[1]: "front_sub_text",
    LABEL_DICT[2]: "back_text",
    LABEL_DICT[3]: "back_sub_text",
    LABEL_DICT[4]: "tag",
    LABEL_DICT[5]: "both_sides",
}


class SampleApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.maxsize(900, 600)
        self.minsize(200,200)
        self.switch_frame(StartPage, "pack",expand=True,fill="both")

    


    def switch_frame(self, frame_class,layout,**kwargs):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        getattr(self._frame,layout)(**kwargs)

class StartPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent,bg="red")
        label = Label(self, text="Flashcard tool", font=('Times 24'))
        label.pack(anchor="n")
        button1 = Button(self, text="Show cards",
                            command=lambda: parent.switch_frame(ShowCardsPage,"grid"))
        button2 = Button(self, text="Add cards",
                            command=lambda: parent.switch_frame(AddCardsPage,"grid"))
        button3 = Button(self, text="Import cards",
                            command=lambda: parent.switch_frame(ImportCardsPage,"pack"))
        button1.pack(padx=5,pady=5,side="right",anchor="s")
        button2.pack(padx=5,pady=5,side="right",anchor="s")
        button3.pack(padx=5,pady=5,side="right",anchor="s")




class AddCardsPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent,width=200, height=400)
        self.parent = parent
        entries_dict = {}
        for i in range(5):
            self.columnconfigure(i, weight=1, minsize=10)
            self.rowconfigure(i, weight=1, minsize=50)
            label = Label(self, text=LABEL_DICT[i])
            entry = Entry(self)
            label.grid(row=i, column=0, padx=5, pady=5)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries_dict[LABEL_DICT[i]] = entry

        both_sides_var = BooleanVar(self)
        both_sides_check = Checkbutton(self, text="Both sides card",variable=both_sides_var)
        both_sides_check.grid(row=5, column=0, padx=5, pady=5)
        entries_dict["Both sides"] = both_sides_var
        save_func = partial(self._save_button, entries_dict=entries_dict)
        save_button = Button(self,text="Save card", command=save_func)
        home = Button(self,text="<-",command=lambda: parent.switch_frame(StartPage,"pack",expand=True,fill="both"))
        save_button.grid(row=6, column=0, padx=5, pady=5)
        home.grid(row=6, column=1, padx=5, pady=5)


    def _check_minimum_to_save(self, entries_dict: Dict[str,Entry]) -> bool:
        if not entries_dict[LABEL_DICT[0]].get() or not entries_dict[LABEL_DICT[2]].get():
            messagebox.showerror("Error", "You must add a front and a back text")
            return False
        return True


    def _save_button(self,entries_dict: Dict[str,Entry]):
        if not self._check_minimum_to_save(entries_dict):
            return 
        kwargs = {}
        for entry in entries_dict:
            val = entries_dict[entry].get()
            attr_name = ATTR_DICT[entry]
            kwargs[attr_name] = val
            try:
                entries_dict[entry].delete(0,"end")
            except AttributeError:
                pass
        
        card = Card(**kwargs)

        with Session.begin() as session:
            card.save_to_database(session)
            messagebox.showinfo("Info","Card added")


class ShowCardsPage(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)
        home = Button(self,text="<-",command=lambda: parent.switch_frame(StartPage,"pack",expand=True,fill="both"))
        home.grid()


class ImportCardsPage(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)
        home = Button(self,text="<-",command=lambda: parent.switch_frame(StartPage,"pack",expand=True,fill="both"))
        home.pack()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()


