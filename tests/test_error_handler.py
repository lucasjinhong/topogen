import pytest

from topogen.utils.error_handler import *


def test_err_raise():
    '''
    Test the err_raise function.
    '''

    # Test the error raise
    with pytest.raises(ValueError, match='This is a test'):
        err_raise(ValueError, 'This is a test', True)

    # Test the error not raise
    err_raise(ValueError, 'This is a test', False)