class InactiveSessionError(Exception):
    pass

def get_session_info(session_id):
    return {"session_id": session_id, "active": True}

def persist_session(session_info):
	pass

def update_session_id(session_id):
    """
        regenerate the session id and persist it with the existing session info
    """
    return session_id
