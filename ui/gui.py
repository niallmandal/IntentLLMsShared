import tkinter as tk


class IntentApp:
    def __init__(self, root):
        self.root = root
        self.process_callback = None
        self.configure_window()
        self.create_widgets()

    def configure_window(self):
        self.root.title("Intent Stuff")
        self.root.configure(bg="white")
        width = 600
        height = 500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.root.geometry(alignstr)


import tkinter as tk


class IntentApp:
    def __init__(self, root):
        self.root = root
        self.process_callback = None
        self.configure_window()
        self.create_widgets()

    def configure_window(self):
        self.root.title("Intent Stuff")
        self.root.configure(bg="white")
        width = 600
        height = 500
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.root.geometry(alignstr)

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(expand=True)

        self.input_field = tk.Entry(
            frame,
            justify="center",
            bd=0,
            highlightthickness=1,
            highlightbackground="black",
            bg="white",
            fg="black",
            insertbackground="black",
        )
        self.input_field.pack(padx=10, pady=(10, 0))

        underline = tk.Frame(frame, height=2, bg="black", bd=0)
        underline.pack(fill="x", padx=10)

        submit_button = tk.Button(
            frame,
            text="Submit",
            command=self.on_submit,
            cursor="hand2",
            fg="black",
            bg="white",
            relief="flat",
            highlightthickness=0,
        )
        submit_button.pack(padx=10, pady=10)

        self.output_label = tk.Label(
            frame,
            text="Please enter something!",
            bg="white",
            fg="black",
            font=("Courier", 10),
        )
        self.output_label.pack(padx=10, pady=10)

    def on_submit(self):
        if self.process_callback:
            user_input = self.input_field.get()
            self.process_callback(self, user_input)
        else:
            print("Process callback not set!")

    def set_process_callback(self, callback):
        self.process_callback = callback
        
    def update_output(self, output_text):
        self.output_label.config(text=output_text)


def main():
    root = tk.Tk()
    app = IntentApp(root)
    app.set_process_callback(
        lambda user_input: app.set_output_text(f"Processing: {user_input}")
    )
    root.mainloop()


if __name__ == "__main__":
    main()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(expand=True)

        self.input_field = tk.Entry(
            frame,
            justify="center",
            bd=0,
            highlightthickness=0,
            fg="black",
            insertbackground="black",
        )
        self.input_field.pack(padx=10, pady=(10, 0))

        underline = tk.Frame(frame, height=2, bg="black", bd=0)
        underline.pack(fill="x", padx=10)

        submit_button = tk.Button(
            frame,
            text="Submit",
            command=self.on_submit,
            cursor="hand2",
            fg="black",
            bg="white",
        )
        submit_button.pack(padx=10, pady=10)

        self.output_label = tk.Label(
            frame,
            text="Please enter something!",
            bg="white",
            fg="black",
            font=("Courier", 10),
        )
        self.output_label.pack(padx=10, pady=10)

    def on_submit(self):
        if self.process_callback:
            user_input = self.input_field.get()
            self.process_callback(user_input)
        else:
            print("Process callback not set!")

    def set_process_callback(self, callback):
        self.process_callback = callback

    def set_output_text(self, text):
        """Sets the output label's text to the provided JSON string."""
        self.output_label.config(text=text)


def main():
    root = tk.Tk()
    app = IntentApp(root)
    app.set_process_callback(
        lambda user_input: app.set_output_text(f"Processing: {user_input}")
    )
    root.mainloop()


if __name__ == "__main__":
    main()
