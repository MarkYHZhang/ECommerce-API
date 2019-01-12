from django.http import HttpResponse


def raw_response(string):
    return "{\"response\": \""+string.upper().replace(" ", "_")+"\"}";


def response(string):
    return HttpResponse(raw_response(string))


def missing(string):
    return response("Missing " + string)


def empty(string):
    return response("Empty " + string)


def invalid(string):
    return response("Invalid " + string)

