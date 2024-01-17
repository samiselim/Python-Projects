def swap_y_z(data: list[str], shift = 0):
    spar = list(reversed(["( SPAR END )", "( SPAR EXIT )", "( SPAR CIRCLE )", "( SPAR START )"]))
    spar_counter = 0
    new_data = []
    for line in data:
        if line.startswith("G1 "):
            new_line = line.split()
            temp = line.split()
            new_line[2] = "y" + str(round(shift+2*32.97-round(float(temp[2][1:]), 2), 2))
            new_line[4] = "z" + str(round(shift+2*32.97-round(float(temp[4][1:]), 2), 2))
            line = " ".join(new_line) + "\n"
        else:
            line = spar[spar_counter]
            spar_counter += 1
            line += "\n"
        new_data.append(line)
    return "".join(new_data)

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def submit():
    global file_name
    with open(file_name, "r") as f:
        file = f.read()

    bottom = "( BOTTOM SECTION )"
    top = "( TOP SECTION )"
    pre_exit = "( PRE-EXIT )"

    try:
        shift = float(shift_data.get())
    except:
        shift = 0

    bottom_data = swap_y_z(list(reversed(file.split(bottom)[1].split(top)[0].split("\n")[1:-1])), shift)
    top_data = swap_y_z(list(reversed(file.split(top)[1].split(pre_exit)[0].split("\n")[1:-1])), shift)
    print(shift)

    [f0, rest] = file.split(bottom)
    [_, rest] = rest.split(top)
    [_, f3] = rest.split(pre_exit)

    new_data = f0 + top + "\n" + top_data + bottom + "\n" + bottom_data + pre_exit + f3

    new_name = "Reverse_" + file_name.split(r"/")[-1]
    temp = file_name.split(r"/")
    temp.pop()
    temp.append(new_name)
    full_name = "/".join(temp)
    with open(full_name, "w") as f:
        f.write(new_data)
    


def select_file():
    global file_name
    file_name = filedialog.askopenfilename()
    print(file_name)


root = tk.Tk()
root.title("Wing reverse")

select_file_label = tk.Label(root, text="Select file:")
select_file_label.pack()
select_file_button = tk.Button(root, text="NGC", command=select_file)
select_file_button.pack()

shift_label = tk.Label(root, text="shift up")
shift_label.pack()
shift_data = tk.Entry(root)
shift_data.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()