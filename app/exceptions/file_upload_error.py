class FileUploadError(Exception):
    def __init__(self, code: str, message: str, file_path: str):
        self.code = code
        self.file_path = file_path
        self.message = message
        super.__init__(f"File upload error: code={self.code}, message={self.message}, file_path={file_path}")
