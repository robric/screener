import requests

method: str = 'POST'

resp = {
"GET":requests.get,
"POST":requests.post,
"DELETE":requests.delete,
}.get(method,"GET")

print (resp)

a = {
    "a":1,
    "b":2,
    "c":3
}.get('a')

print ()