# FileManager class for handling file operations with Lark API
# Provides methods for uploading files to Lark Drive and downloading files from URLs
# Uses rate limiting via semaphore to prevent overloading
import datetime
import time
from lark_oapi.api.drive.v1 import *
from .TenantManager import TenantManager
from app.exceptions.file_upload_error import FileUploadError
import os
import asyncio
from app.src.lark import Lark
import requests

class FileManager:
    def __init__(self, lark_client: Lark, bitable_token: str):
        # Initialize FileManager with Lark client and bitable token
        self.lark = lark_client.client
        self.bitable_token = bitable_token
        self.recording_directory = "data"
        self.semaphore = asyncio.Semaphore(4)

    def download_url(self, url, file_name):
        # Download a file from a URL and save it locally
        response = requests.get(url)

        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully and saved as {file_name}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")

    async def upload_async(self, file_path):
        # Check if file exists, return early if not
        if not os.path.exists(file_path):
            return
            
        # Extract just the filename from the full path
        filename = os.path.split(file_path)[1]

        # Get the file size in bytes
        size = self.get_file_size(file_path)

        # Open the file in binary read mode
        file = open(file_path, 'rb')

        # Build the upload request object with:
        # - filename: name of file to upload
        # - parent_type: specify this is for bitable
        # - parent_node: the bitable token for authentication
        # - size: file size in bytes
        # - file: the actual file object
        request: UploadAllMediaRequest = UploadAllMediaRequest.builder() \
            .request_body(UploadAllMediaRequestBody.builder()
                .file_name(filename)
                .parent_type("bitable_file")
                .parent_node(self.bitable_token)
                .size(size) \
                .file(file) \
                .build()) \
            .build()

        # Make async API call to upload the file
        response: UploadAllMediaResponse = await self.lark.drive.v1.media.aupload_all(request)

        # Check if upload failed (non-zero code means error)
        if response.code != 0:
            raise FileUploadError(
                code=response.code, 
                message=response.msg, 
                file_path=file_path
            )

        # Return the file token that can be used to reference this file
        return response.data.file_token

    async def upload_async_copy(self, file_path):
        # Copy of upload_async method, likely for redundancy or testing
        if not os.path.exists(file_path):
            return
        filename = os.path.split(file_path)[1]
        file = open(file_path, 'rb')

        size = self.get_file_size(file_path)

        request: UploadAllMediaRequest = UploadAllMediaRequest.builder() \
            .request_body(UploadAllMediaRequestBody.builder()
                .file_name(filename)
                .parent_type("bitable_file")
                .parent_node(self.bitable_token)
                .size(size)
                .file(file)
                .build()) \
            .build()

        response: UploadAllMediaResponse = await self.lark.drive.v1.media.aupload_all(request)

        if response.code != 0:
            raise FileUploadError(
                code=response.code, 
                message=response.msg, 
                file_path=file_path
            )

        return response.data.file_token

    def upload(self, file_path):
        # Synchronous version of file upload to Lark Drive
        if not os.path.exists(file_path):
            return
        filename = os.path.split(file_path)[1]
        file = open(file_path, 'rb')

        size = self.get_file_size(file_path)

        request: UploadAllMediaRequest = UploadAllMediaRequest.builder() \
            .request_body(UploadAllMediaRequestBody.builder()
                .file_name(filename)
                .parent_type("bitable_file")
                .parent_node(self.bitable_token)
                .size(size)
                .file(file)
                .build()) \
            .build()

        response: UploadAllMediaResponse = self.lark.drive.v1.media.upload_all(request)

        if response.code != 0:
            raise FileUploadError(
                code=response.code, 
                message=response.msg, 
                file_path=file_path
            )

        return response.data.file_token

    def get_file_size(self, filepath):
        # Get the size of a file in bytes
        try:
            with open(filepath, 'rb') as file:
                file.seek(0, 2)  # Move the file pointer to the end of the file
                file_size = file.tell()  # Get the current position, which is the file size
                return file_size
        except FileNotFoundError:
            return None