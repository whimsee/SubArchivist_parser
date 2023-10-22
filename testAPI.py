import requests

books_url_get = "http://192.168.1.140:6875/api/books"
books_url_post = "http://192.168.1.140:6875/api/books"
books_url_delete = "http://192.168.1.140:6875/api/books/5"
books_url_create = "http://192.168.1.140:6875/api/pages"
API_ID_TOKEN = "7vNfTCteriMBDfUEt6C99Q0qpKwCuSq2:glrRS2kWj0jdhTJ5pBQ4D8Bw0NvEKj2i"

api_url = books_url_post
headers = {"Authorization": "Token " + API_ID_TOKEN}

## GET
# api_url = books_url_get
# response = requests.get(api_url, headers=headers)
# print(response.json())

## POST BOOK
# api_url = books_url_post
# todo = {
#   "name": "My own book",
#   "description": "This is my own little book"
# }
# response = requests.post(api_url, json=todo, headers=headers)

## POST PAGE
ID = "1"
api_url = books_url_create
todo = {
	"book_id": ID,
	"name": "Episode name",
	"markdown": "**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;The royal capital's in sight.<br>"
                "**HEITER**<br>&nbsp;&nbsp;&nbsp;&nbsp;The adventurers are making<br>&nbsp;&nbsp;&nbsp;&nbsp;their triumphant return.<br>"
                "**FRIEREN**<br>&nbsp;&nbsp;&nbsp;&nbsp;Are you trying to put on<br>&nbsp;&nbsp;&nbsp;&nbsp;a brave face again, Heiter?<br>",
	"priority": 15,
	"tags": [
		{"name": "Category", "value": "Not Bad Content"},
		{"name": "Rating", "value": "Average"}
	]
}
response = requests.post(api_url, json=todo, headers=headers)
print(response.json())

## DELETE
# api_url = books_url_delete
# response = requests.delete(api_url, headers=headers)

#print(response.headers)
# print(response.json())
print(response.status_code)