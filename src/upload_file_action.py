from src.action import Action
from src.http_service import HTTPService
from base64 import b64encode
from typing import Any

class UploadFileAction(Action):
    def run(self, args: dict[str, Any]) -> str:
        # Base64 encode the requested file content
        content = '' 
        with open(args['filename'], 'r') as f:
            content = b64encode(f.read().encode()).decode()

        # Craft and send the request
        request = {
            'action': 'upload_file',
            'args': {
                'filename': args['filename'],
                'content': content
            }
        }
        HTTPService().send_request(request)

        # Return empty string
        return ''
