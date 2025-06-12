from src.action import Action
from src.http_service import HTTPService
from base64 import b64encode
from typing import Any

class UploadFileAction(Action):
    def run(self, args: dict[str, Any]) -> str:
        content = None

        # Read and base64 encode the appropriate file. The mode depends on if the file is
        # binary or not
        if args['binary']:
            with open(args['filename'], 'rb') as f:
                content = b64encode(f.read()).decode()
        else:
            with open(args['filename'], 'r') as f:
                content = b64encode(f.read().encode()).decode()

        # Craft and send the request
        request = {
            'action': 'upload_file',
            'args': {
                'filename': args['filename'],
                'content': content,
                'binary': args['binary']
            }
        }
        HTTPService().send_request(request)

        # Return empty string
        return ''
