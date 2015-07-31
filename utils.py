def pp(jsonObject):
    ''' Pretty prints json '''
    print json.dumps(jsonObject, indent=4)

# Could optimize this
def get_territory_by_id(tid, territories):
    for t in territories:
        if t['territory'] == tid:
            return t
    return None

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped