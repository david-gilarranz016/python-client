from src.action import Action
from src.http_service import HTTPService

class DownloadFileAction(Action):
    def run(self, args: dict[str, str]) -> str:
        # Create and send request
        request = {
            'action': 'download_file',
            'args': {
                'filename': args['filename']
            }
        }
        response = HTTPService().send_request(request)
        return ''
