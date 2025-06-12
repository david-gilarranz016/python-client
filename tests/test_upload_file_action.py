from src.action import Action
from src.upload_file_action import UploadFileAction
from src.http_service import HTTPService

import pytest
import pyfakefs

################################################################################
#                                                                              #
# Fixtures -> used for setup and teardown                                      #
#                                                                              #
################################################################################

################################################################################
#                                                                              #
# Test cases                                                                   #
#                                                                              #
################################################################################

def test_is_action() -> None:
    assert issubclass(UploadFileAction, Action)
