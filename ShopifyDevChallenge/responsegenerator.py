from django.http import HttpResponse

def response(string):
    return HttpResponse("{\"response\": \""+string.upper().replace(" ", "_")+"\"}")


def missing(string):
    return response("Missing " + string)


def empty(string):
    return response("Empty " + string)


def invalid(string):
    return response("Invalid " + string)

