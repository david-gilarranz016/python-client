from client.action import Action
from client.http_service import HTTPService

import os
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

        # Keep only basename
        basename = os.path.basename(args['filename'])

        # Create binary or text output file
        if (args['binary']):
            with open(basename, 'wb') as f:
                decoded_content = b64decode(response['output'].encode())
                f.write(decoded_content)
        else:
            with open(basename, 'w') as f:
                decoded_content = b64decode(response['output'].encode()).decode()
                f.write(decoded_content)

        return ''

