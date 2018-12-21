"""
@author: Julian Sobott
@created: 21.12.2018
@brief: Watch for file changes and updates release
@description:
Start: creates complete release
On change: copy file or handle html
@external_use:

@internal_use:

"""
import threading
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import os
import sys
import time
import shutil


from Logging import logger
import Release
import Paths
from CMD import *

DESCRIPTION = (
    "" + __file__ + "\n"
    "This script automatically releases on file changes.\n"
    "For more information about the release module view the docs." 
    "Following arguments are optional:\n\n"
    "  {src=[src_path]}: You can add a path relative to the dev path. Only files inside this paths are handled"
    "\n")


def start(src_path=None):
    watch_path = Paths.Website.ABS_DEV_PATH
    if src_path:
        watch_path = os.path.join(watch_path, src_path)
    Release.create_release(src_path=src_path, clear_release_first=True)
    watcher = threading.Thread(target=watch_local_changes, args=(watch_path,), name="Watcher")
    watcher.start()


def watch_local_changes(dev_path):
    logger.info("Start auto release on change")
    logger.info("While console is open, all changes result in auto release")
    observer = Observer()
    observers = []

    if os.path.exists(dev_path):
        event_handler = ChangeEventHandler(dev_path)
        observer.schedule(event_handler, dev_path, recursive=True)
        observers.append(observer)
    else:
        logger.warning("Path does not exist, (%s)", dev_path)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.unschedule_all()
            observer.stop()

    for observer in observers:
        observer.join()


class ChangeEventHandler(PatternMatchingEventHandler):

    def __init__(self, path):
        super().__init__(ignore_patterns=[".sass"])
        self.path = path
        self.project_path = os.path.split(path)[0]

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            extension = os.path.splitext(file_path)[1]
            Release.handle_file(file_path, self.project_path, file_extension=extension)

    def on_deleted(self, event):
        file_path = event.src_path
        release_file_path = Release.dev_to_release_path(file_path, self.project_path)
        if event.is_directory:
            shutil.rmtree(release_file_path, ignore_errors=True)
        else:
            try:
                os.remove(release_file_path)
            except FileNotFoundError:
                pass

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            extension = os.path.splitext(file_path)[1]
            if extension in Release.IMPORT_EXTENSIONS:
                Release.create_release(just_imports=True)
            else:
                Release.handle_file(file_path, self.project_path, file_extension=extension)

    def on_moved(self, event):
        # TODO: handle directories
        src_file_path = event.src_path
        dest_file_path = event.dest_path
        src_release_file_path = Release.dev_to_release_path(src_file_path, self.project_path)
        dest_release_file_path = Release.dev_to_release_path(dest_file_path, self.project_path)

        if self.path in dest_release_file_path:
            shutil.move(src_release_file_path, dest_release_file_path)
        else:
            try:
                os.remove(src_release_file_path)
            except FileNotFoundError:
                pass


def print_help():
    print(DESCRIPTION)


def handle_sys_arguments(all_args):
    help_arg = ["--help", "-h", "?"]
    named_src_folder_arg = ["src"]

    if intersects(help_arg, all_args):
        print_help()
        exit(0)

    src_folder = get_optional_parameter(named_src_folder_arg, all_args)
    start(src_path=src_folder)


if __name__ == "__main__":
    num_args = len(sys.argv) - 1
    if num_args > 0:
        all_args = sys.argv[1:]
    else:
        print_help()
        exit(0)

    p_project_path = all_args[0]
    start(p_project_path)