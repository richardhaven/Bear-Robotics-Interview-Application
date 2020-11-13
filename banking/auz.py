class InsufficientAccessError(Exceptino):
	pass

def check_access(session_info, context, *args, **kwargs):
    if not does_have_access(session_info, context, args, kwargs):
        log_auz_violation(session_info, context)
        raise InsufficientAccessError()

def does_have_access(session_info, context, *args, **kwargs):
	pass

def log_auz_violation(session_info, context):
	pass
