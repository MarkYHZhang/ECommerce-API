def response(string):
    return {"response": string}


def missing(string):
    return response("Missing " + string)


def empty(string):
    return response("Empty " + string)


def invalid(string):
    return response("Invalid " + string)

