from src.action import Action
from src.http_service import HTTPService

from base64 import b64decode
from typing import Any

class DownloadFileAction(Action):
    def run(self, args: dict[str, Any]) -> str:
        # Create and send request
        request = {
            'action': 'download_file',
            'args': {
                'filename': args['filename'],
                'binary': args['binary']
            }
        }

        # Read response
        response = HTTPService().send_request(request)

        # Create binary or text output file
        if (args['binary']):
            with open(args['filename'], 'wb') as f:
                decoded_content = b64decode(response['output'].encode())
                f.write(decoded_content)
        else:
            with open(args['filename'], 'w') as f:
                decoded_content = b64decode(response['output'].encode()).decode()
                f.write(decoded_content)

        return ''

