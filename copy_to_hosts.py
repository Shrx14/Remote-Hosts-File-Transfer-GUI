import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import csv
import os
from datetime import datetime
import threading

class CopyToHostsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Copy File to Hosts")

        # IPs/Hostnames input
        tk.Label(root, text="Enter IP addresses / Hostnames (one per line):").grid(row=0, column=0, sticky="w")
        self.hosts_text = tk.Text(root, height=10, width=50)
        self.hosts_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Source file selection
        tk.Label(root, text="Select file to copy:").grid(row=2, column=0, sticky="w")
        self.source_entry = tk.Entry(root, width=40)
        self.source_entry.grid(row=3, column=0, padx=5, pady=5)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=3, column=1, padx=5, pady=5)

        # Destination path input
        tk.Label(root, text="Enter destination path (relative to host):").grid(row=4, column=0, sticky="w")
        self.dest_entry = tk.Entry(root, width=50)
        self.dest_entry.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Copy button
        self.copy_button = tk.Button(root, text="Copy File", command=self.start_copy_thread)
        self.copy_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Status label
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.grid(row=7, column=0, columnspan=3)

        # Log file path
        self.log_file = "copy_log.csv"
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Datetime", "Host", "FileCopied", "DestinationPath", "Status"])

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, file_path)

    def start_copy_thread(self):
        # Start the copy operation in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.copy_file_to_hosts)
        thread.start()

    def copy_file_to_hosts(self):
        import threading

        # Disable copy button and show loading text
        self.root.after(0, lambda: self.copy_button.config(state=tk.DISABLED, text="Copying..."))

        # Clear status label on new copy attempt
        self.root.after(0, lambda: self.status_label.config(text=""))

        hosts = self.hosts_text.get("1.0", tk.END).strip().splitlines()
        source_file = self.source_entry.get().strip()
        dest_path = self.dest_entry.get().strip()

        if not hosts:
            self.root.after(0, lambda: messagebox.showerror("Error", "Please enter at least one IP address or hostname."))
            self.root.after(0, lambda: self.copy_button.config(state=tk.NORMAL, text="Copy File"))
            return
        if not source_file or not os.path.isfile(source_file):
            self.root.after(0, lambda: messagebox.showerror("Error", "Please select a valid source file."))
            self.root.after(0, lambda: self.copy_button.config(state=tk.NORMAL, text="Copy File"))
            return
        if not dest_path:
            self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a destination path."))
            self.root.after(0, lambda: self.copy_button.config(state=tk.NORMAL, text="Copy File"))
            return

        success_count = 0
        skipped_count = 0
        success_count_lock = threading.Lock()
        skipped_count_lock = threading.Lock()

        def copy_to_host(host):
            nonlocal success_count, skipped_count
            host = host.strip()
            if not host:
                return
            unc_path = f"\\\\{host}\\{dest_path.replace('/', '\\')}"
            try:
                os.makedirs(unc_path, exist_ok=True)
                shutil.copy2(source_file, unc_path)
                status = "Success"
                with success_count_lock:
                    success_count += 1
            except Exception as e:
                status = f"Skipped: {str(e)}"
                with skipped_count_lock:
                    skipped_count += 1

            try:
                with open(self.log_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), host, os.path.basename(source_file), unc_path, status])
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Logging Error", f"Failed to write to log file: {str(e)}"))

        threads = []
        for host in hosts:
            t = threading.Thread(target=copy_to_host, args=(host,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.root.after(0, lambda: self.status_label.config(text=f"Copy completed: {success_count} success, {skipped_count} skipped."))
        self.root.after(0, lambda: messagebox.showinfo("Copy Completed", f"Copy completed:\n{success_count} success\n{skipped_count} skipped"))
        self.root.after(0, lambda: self.copy_button.config(state=tk.NORMAL, text="Copy File"))

if __name__ == "__main__":
    root = tk.Tk()
    app = CopyToHostsApp(root)
    root.mainloop()
