import os
import time
import tkinter as tk
from tkinter import ttk
from gologin import GoLogin
import threading

class GoLoginGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("GoLogin Profile Creator")
        self.master.configure(bg="green")

        self.token_label = ttk.Label(master, text="Token:", background="green")
        self.token_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.token_entry = ttk.Entry(master, width=40)
        self.token_entry.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

        self.profile_name_label = ttk.Label(master, text="Profile Name:", background="green")
        self.profile_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.profile_name_entry = ttk.Entry(master, width=40)
        self.profile_name_entry.grid(row=3, column=0, padx=5, pady=5, columnspan=3)

        self.num_profiles_label = ttk.Label(master, text="Number of Profiles:", background="green")
        self.num_profiles_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.num_profiles_entry = ttk.Entry(master, width=40)
        self.num_profiles_entry.grid(row=5, column=0, padx=5, pady=5, columnspan=3)

        self.start_button = ttk.Button(master, text="Start", command=self.start_profile_creation, style="Blue.TButton")
        self.start_button.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_profile_creation, style="Red.TButton", state="disabled")
        self.stop_button.grid(row=6, column=2, padx=5, pady=5, sticky="w")

        self.output_text = tk.Text(master, height=10, width=50, bg="orange")
        self.output_text.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.gl = None
        self.profile_creation_running = False

    def start_profile_creation(self):
        token = self.token_entry.get().strip()
        num_iterations = int(self.num_profiles_entry.get().strip())
        profile_name = self.profile_name_entry.get().strip()

        if token and num_iterations and profile_name:
            self.gl = GoLogin({"token": token})
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.profile_creation_running = True
            threading.Thread(target=self.create_profiles, args=(profile_name, num_iterations)).start()
        else:
            self.print_output("Please fill in all fields.")

    def stop_profile_creation(self):
        self.profile_creation_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.print_output("Profile creation stopped.")

    def create_profiles(self, profile_name, num_iterations):
        try:
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            path = os.path.join(desktop_path, f'{profile_name}')

            if not os.path.exists(path):
                os.makedirs(path)


            num_existing_profiles = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
            total_profiles_created = num_existing_profiles
            for i in range(num_iterations):
                if not self.profile_creation_running:
                    break

                if self.gl:
                    profile_id = self.gl.create({
                        "name": f"profile_{total_profiles_created + i + 1}",
                        "os": "mac",
                        "navigator": {
                            "language": "en-US",
                            "userAgent": "random",
                            "resolution": "1024x768",
                            "platform": "win",
                        },
                        "proxyEnabled": False,
                        "proxy": {
                            "mode": "gologin",
                            "autoProxyRegion": "us"
                        },
                        "webRTC": {
                            "mode": "alerted",
                            "enabled": True,
                        },
                    })

                    file_number = f"{profile_id}.txt"
                    text_file_path = os.path.join(path, file_number)
                    with open(text_file_path, "w") as f:
                        f.write(str(i + 1))
                        self.print_output(f"Profile {total_profiles_created + i + 1} created: {profile_id}")

                    time.sleep(1)  # Add a delay to avoid rate limiting
                    self.master.update_idletasks()
                else:
                    self.print_output("GoLogin object is not initialized.")

            self.profile_creation_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.print_output("Creation of accounts is finished.")

        except Exception as e:
            self.print_output(f"An error occurred: {e}")
            # Retry creating profiles

    def print_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

def main():
    root = tk.Tk()
    style = ttk.Style(root)
    style.configure("Blue.TButton", foreground="white", background="blue", relief=tk.RAISED, borderwidth=3)
    style.configure("Red.TButton", foreground="white", background="red", relief=tk.RAISED, borderwidth=3)
    app = GoLoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
