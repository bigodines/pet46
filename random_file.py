import argparse
import os
from random import choice


class RandomFile:
    def __init__(self, directory, file_type):
        self.directory = directory
        self.file_type = file_type

    def get_random_file(self):
        files = self.get_files()
        if not files:
            return "No files found"
        return choice(files)

    def get_files(self):
        if not os.path.isdir(self.directory):
            raise ValueError(f"Directory '{self.directory}' does not exist.")

        files = []
        for root, _, filenames in os.walk(self.directory):
            for filename in filenames:
                if filename.endswith(
                    tuple(self.type_to_extension())
                ) and not filename.startswith("."):
                    files.append(os.path.join(root, filename))

        if not files:
            print(f"No files of type '{self.file_type}' found in '{self.directory}'")
        return files

    def type_to_extension(self):
        types = {
            "audio": (".mp3", ".wav", ".flac"),
            "video": (".mp4", ".mkv", ".avi", ".flv"),
            "image": (".jpg", ".jpeg", ".png", ".gif"),
        }
        if self.file_type in types:
            return types[self.file_type]
        else:
            raise ValueError(
                f"Unsupported file type '{self.file_type}'. Choose from 'audio', 'video', or 'image'."
            )

    def __repr__(self):
        return f'RandomFile(directory="{self.directory}", file_type="{self.file_type}")'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pick a random file in a directory")
    parser.add_argument("--dir", help="Directory to search for files")
    parser.add_argument("--type", help="File type (audio, video, image)")

    args = parser.parse_args()
    directory = args.dir
    file_type = args.type

    random_file = RandomFile(directory, file_type)

    try:
        # result!
        print("Random file selected:", random_file.get_random_file())
    except ValueError as e:
        print(e)
