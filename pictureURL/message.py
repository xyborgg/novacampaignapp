
import json

import requests

url = "https://www.bulksmsnigeria.com/api/v1/sms/create"

# https://www.bulksmsnigeria.com/api/v1/sms/create?, api_token=BS53DO6EEptDoMNF6y79doLPdSuJlT5FzMkB22HdGq9FvJLR4SCyxZlNnH6D&,
# from=BulkSMS.ng&to=2348063113913&\
#                    body=Welcome&dnd=2



def sendPostRequest(requrl, api_token ,FROM, to, body):
    req_params = {
        "api_token": api_token,
        "from": FROM,
        "to": to,
        "body": body
    }

    return requests.post(requrl, req_params)


# response = sendPostRequest(url, "P0KpZxWPZwOIT6JIKEBCFOFE6Q12ztUrsbCoxdE2ppfsXRwqAUyx3kEvTYFy", "Efiong", "2348121891955", "api-connection test from my application" )

# print(response.text)