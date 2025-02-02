import tkinter as tk

root = tk.tk()
button = tk.Button(root, text='Click me!', command=lambda:print('Click me!'))
button.pack()
root.mainloop()