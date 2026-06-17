import json

def success_response(data=None, message="Success", status_code=200):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "success": True,
            "message": message,
            "data": data
        })
    }

def error_response(message="An error occurred", status_code=400):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "success": False,
            "message": message,
            "data": None
        })
    }