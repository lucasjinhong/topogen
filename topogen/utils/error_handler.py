def err_raise(err_type, err_msg, err_reason):
    '''
    An error handler function to raise error

    Args:
        err_type (str): the type of the error
        err_msg (str): the message of the error
        err_reason (str, bool): the reason of the error
    '''

    if err_reason:
        raise err_type(str(err_reason) + ': ' + err_msg)