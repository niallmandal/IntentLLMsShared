import tkinter as tk
from ui.gui import IntentApp 
import json

from test import convert_transaction  

swap_schema_path = 'swap.json'
limit_order_schema_path = 'limit_swap.json'

with open(swap_schema_path, 'r') as file:
    swap_schema = json.load(file)

with open(limit_order_schema_path, 'r') as file:
    limit_order_schema = json.load(file)

def process_user_input(app, user_input):
    """
    Callback function to process the user input from the GUI.
    """
    if user_input.strip(): 
        filled_schema = convert_transaction(user_input, swap_schema, limit_order_schema)
        json_output = json.dumps(filled_schema, indent=4)
        app.update_output(json_output)

    else:
        print("Please enter some transaction text.")

def main():
    root = tk.Tk()
    app = IntentApp(root)
    app.set_process_callback(process_user_input)
    
    root.mainloop()

if __name__ == "__main__":
    main()
