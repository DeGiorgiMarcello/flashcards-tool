from tkinter import (
    Label,
    Tk,
    Button,
    Entry,
    messagebox,
    Checkbutton,
    BooleanVar,
    font,
    Frame,
)
from typing import Dict
from datetime import date
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
        self.minsize(200, 200)
        self.switch_frame(StartPage, "pack", expand=True, fill="both")

    def switch_frame(self, frame_class, layout, **kwargs):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        getattr(self._frame, layout)(**kwargs)

    def show_widget(self, widget, layout, **kwargs):
        getattr(widget, layout)(**kwargs)


class StartPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        label = Label(self, text="Flashcard tool", font=("Times 24"))
        label.pack(anchor="n")
        button1 = Button(
            self,
            text="Show cards",
            command=lambda: parent.switch_frame(
                ShowCardsPage, "pack", expand=True, fill="both"
            ),
        )
        button2 = Button(
            self,
            text="Add cards",
            command=lambda: parent.switch_frame(
                AddCardsPage, "pack", expand=True, fill="both"
            ),
        )
        button3 = Button(
            self,
            text="Import cards",
            command=lambda: parent.switch_frame(
                ImportCardsPage, "pack", expand=True, fill="both"
            ),
        )
        button1.pack(padx=5, pady=5, side="right", anchor="s")
        button2.pack(padx=5, pady=5, side="right", anchor="s")
        button3.pack(padx=5, pady=5, side="right", anchor="s")


class AddCardsPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, width=200, height=400)
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
        both_sides_check = Checkbutton(
            self, text="Both sides card", variable=both_sides_var
        )
        both_sides_check.grid(row=5, column=0, padx=5, pady=5)
        entries_dict["Both sides"] = both_sides_var
        save_func = partial(self._save_button, entries_dict=entries_dict)
        save_button = Button(self, text="Save card", command=save_func)
        home = Button(
            self,
            text="<-",
            command=lambda: parent.switch_frame(
                StartPage, "pack", expand=True, fill="both"
            ),
        )
        save_button.grid(row=6, column=0, padx=5, pady=5)
        home.grid(row=6, column=1, padx=5, pady=5)

    def _check_minimum_to_save(self, entries_dict: Dict[str, Entry]) -> bool:
        if (
            not entries_dict[LABEL_DICT[0]].get()
            or not entries_dict[LABEL_DICT[2]].get()
        ):
            messagebox.showerror("Error", "You must add a front and a back text")
            return False
        return True

    def _save_button(self, entries_dict: Dict[str, Entry]):
        if not self._check_minimum_to_save(entries_dict):
            return
        kwargs = {}
        for entry in entries_dict:
            val = entries_dict[entry].get()
            attr_name = ATTR_DICT[entry]
            kwargs[attr_name] = val
            try:
                entries_dict[entry].delete(0, "end")
            except AttributeError:
                pass
        card = Card(**kwargs)

        with Session.begin() as session:
            card.save_to_database(session)
            messagebox.showinfo("Info", "Card added")


class ShowCardsPage(Frame):
    def __init__(self, parent):
        self.parent = parent
        self._get_cards_from_db()
        current_card = self.cards.__next__()
        Frame.__init__(self, parent, width=300, height=300, background="red")
        front_frame = Frame(master=self, pady=5, padx=5)
        ft_label = Label(
            master=front_frame, text=current_card.front_text, font=("Times 20")
        )
        ft_sub_label = Label(
            master=front_frame, text=current_card.front_sub_text, font=("Times 16")
        )
        back_frame = Frame(master=self, background="#70dae6", pady=5, padx=5)
        bt_label = Label(
            master=back_frame,
            text=current_card.back_text,
            font=("Times 20"),
            background="#70dae6",
        )
        bt_sub_label = Label(
            master=back_frame,
            text=current_card.back_sub_text,
            font=("Times 16"),
            background="#70dae6",
        )
        ft_label.pack(expand=True)
        ft_sub_label.pack()
        bt_label.pack()
        bt_sub_label.pack()
        button_frame = Frame(self, pady=5, padx=5)
        self._create_show_button(button_frame, back_frame)

        front_frame.pack(expand=True, fill="both")

        button_frame.columnconfigure([0, 1, 2], weight=1)
        button_frame.rowconfigure(0, weight=1)

        button_frame.pack(expand=True, fill="both", side="bottom")

    def _get_cards_from_db(self):
        with Session.begin() as session:
            res = session.query(Card).filter(Card.next_rep <= date.today()).all()
        self.cards = iter(res)

    def _show_back(self, button_frame, **kwargs):
        parent = kwargs.get("parent")
        widget = kwargs.get("widget")
        layout = kwargs.get("layout")
        expand = kwargs.get("expand")
        fill = kwargs.get("fill")

        parent.show_widget(widget=widget, layout=layout, expand=expand, fill=fill)
        for widgets in button_frame.winfo_children():
            widgets.destroy()

        self._create_next_card_button(button_frame)

    def _create_show_button(self, button_frame, back_frame):
        show_btn = Button(
            button_frame,
            text="Show",
            padx=5,
            pady=5,
            command=partial(
                self._show_back,
                button_frame=button_frame,
                parent=self.parent,
                widget=back_frame,
                layout="pack",
                expand=True,
                fill="both",
            ),
        )
        home = Button(
            button_frame,
            text="Home",
            padx=5,
            pady=5,
            command=lambda: self.parent.switch_frame(
                StartPage, "pack", expand=True, fill="both"
            ),
        )

        show_btn.grid(row=0, column=0)
        home.grid(row=0, column=1)

    def _create_next_card_button(self, button_frame):
        got_button = Button(button_frame, padx=5, pady=5, text="Got it!")
        repeat_button = Button(button_frame, padx=5, pady=5, text="Repeat")
        home = Button(
            button_frame,
            text="Home",
            padx=5,
            pady=5,
            command=lambda: self.parent.switch_frame(
                StartPage, "pack", expand=True, fill="both"
            ),
        )
        got_button.grid(row=0, column=0)
        repeat_button.grid(row=0, column=1)
        home.grid(row=0, column=2)


class ImportCardsPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        home = Button(
            self,
            text="<-",
            command=lambda: parent.switch_frame(
                StartPage, "pack", expand=True, fill="both"
            ),
        )
        home.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
