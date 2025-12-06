from fastapi.requests import Request

def log(tag="API", message="", request: Request = None): #request is none by default, if there is a request it will be passed
    with open("log.txt", "a+") as log: #append instead of reqwrite with w+ on each call
        log.write(f"{tag}:{message}\n")
        log.write(f"Request method: {request.method if request else 'No Request'}\n")
        log.write(f"Request url: {request.url if request else 'No Request'}\n")