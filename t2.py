import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, source_path, destination_path):
        super().__init__()
        self.source_path = source_path
        self.destination_path = destination_path

    def on_created(self, event):
        if event.is_directory:
            return
        self.copy_file(event.src_path)

    def copy_file(self, source_path):
        file_name = os.path.basename(source_path)
        destination_file_path = os.path.join(self.destination_path, file_name)

        # Check if the file already exists in the destination
        file_suffix = 1
        while os.path.exists(destination_file_path):
            base_name, extension = os.path.splitext(file_name)
            new_file_name = f"{base_name}_{file_suffix}{extension}"
            destination_file_path = os.path.join(self.destination_path, new_file_name)
            file_suffix += 1

        shutil.copy(source_path, destination_file_path)
        print(f"File {source_path} copied to {destination_file_path}")

def poll_and_copy(source_path, destination_path, polling_interval_ms=100):
    while True:
        files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f))]

        for file in files:
            source_file_path = os.path.join(source_path, file)
            event_handler.copy_file(source_file_path)

        time.sleep(polling_interval_ms / 1000)

def start_file_monitoring(source_path, destination_path):
    global event_handler
    event_handler = FileHandler(source_path, destination_path)
    observer = Observer()
    observer.schedule(event_handler, path=source_path, recursive=False)
    observer.start()

    try:
        poll_and_copy(source_path, destination_path)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    source_path = "C:\Intel\input"  # Replace with the path you want to monitor
    destination_path = "C:\Intel\out"  # Replace with your desired destination path

    start_file_monitoring(source_path, destination_path)
