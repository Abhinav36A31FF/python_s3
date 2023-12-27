import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# this t3
class FileHandler(FileSystemEventHandler):
    def __init__(self, source_path, destination_path, last_execution_time):
        super().__init__()
        self.source_path = source_path
        self.destination_path = destination_path
        self.last_execution_time = last_execution_time

    def on_created(self, event):
        if event.is_directory:
            return
        self.copy_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        self.copy_file(event.src_path)

    def copy_file(self, source_path):
        file_name = os.path.basename(source_path)
        destination_file_path = os.path.join(self.destination_path, file_name)

        # Check if the file was created or modified after the last execution time
        if os.path.getmtime(source_path) > self.last_execution_time:
            # Check if the file already exists in the destination
            file_suffix = 1
            while os.path.exists(destination_file_path):
                base_name, extension = os.path.splitext(file_name)
                new_file_name = f"{base_name}_{file_suffix}{extension}"
                destination_file_path = os.path.join(self.destination_path, new_file_name)
                file_suffix += 1

            shutil.copy(source_path, destination_file_path)
            print(f"File {source_path} copied to {destination_file_path}")

def start_file_monitoring(source_path, destination_path, last_execution_time):
    event_handler = FileHandler(source_path, destination_path, last_execution_time)
    observer = Observer()
    observer.schedule(event_handler, path=source_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    source_path = "C:\Intel\input"  # Replace with the path you want to monitor
    destination_path = "C:\Intel\out"  # Replace with your desired destination path

    # Store the current time as the last execution time
    last_execution_time = time.time()

    start_file_monitoring(source_path, destination_path, last_execution_time)
