from tkinter import Label, Tk, Button, Entry, messagebox, Checkbutton, BooleanVar, Frame, CENTER
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

def _check_minimum_to_save(entries_dict: Dict[str,Entry]) -> bool:
    if not entries_dict[LABEL_DICT[0]].get() or not entries_dict[LABEL_DICT[2]].get():
        messagebox.showerror("Error", "You must add a front and a back text")
        return False
    return True


def _save_button(entries_dict: Dict[str,Entry]):
    if not _check_minimum_to_save(entries_dict):
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


window = Tk()
window.title("Add a flashcard")
# new_card_btn = Button(ro, text="Add flashcard", command=)
# new_card_btn.pack()




entries_dict = {}
for i in range(5):
    window.columnconfigure(i, weight=1, minsize=10)
    window.rowconfigure(i, weight=1, minsize=50)
    label = Label(master=window, text=LABEL_DICT[i])
    entry = Entry(master=window)
    label.grid(row=i, column=0, padx=5, pady=5)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries_dict[LABEL_DICT[i]] = entry

both_sides_var = BooleanVar(master=window)
both_sides_check = Checkbutton(master=window, text="Both sides card",variable=both_sides_var)
both_sides_check.grid(row=5, column=0, padx=5, pady=5)
entries_dict["Both sides"] = both_sides_var
save_func = partial(_save_button, entries_dict=entries_dict)
save_button = Button(master=window,text="Save card", command=save_func)
home = Button(master=window,text="<-")
save_button.grid(row=6, column=0, padx=5, pady=5)
home.grid(row=6, column=1, padx=5, pady=5)


# frame.pack()
window.mainloop()
