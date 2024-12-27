class FileUtils:

    @staticmethod
    def get_extension(file_name: str) -> str:
        return file_name.split(".")[-1]

    @staticmethod
    def get_file_size(size_in_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} PB"
