def messageEntity(msg) -> dict:
    return {
        "_id": msg['_id'],
        "profile":msg["profile"],
        "full_text":msg["full_text"],
    }

def clearedMessageEntity(msg) -> dict:
    return {
        "id": str(msg['_id']),
        "profile": msg["profile"],
        "full_text": msg["full_text"],
        "clean_text":msg["clean_text"],
        "hashtags":msg["hashtags"],
        "mentions":msg["mentions"],
        "urls":msg["urls"],
        "tokens":msg["tokens"],
    }
