import json
import time

import requests

from model import BookManagement

TOKEN = '6122666009:AAH8S7ZBQHT3rPo8ozsNdUKDINjrs5fKOKY'

bookManagement = BookManagement(db_host='172.17.0.1', db_user='root', db_password='123456', db_name='book_chat_bot')


# bookManagement = BookManagement(db_host='192.168.0.237', db_user='root', db_password='123456', db_name='book_chat_bot')


def send_message(chat_id: int, text: str) -> dict:
    """
    Sends a message to the user through the Telegram Bot API.

    Args:
        chat_id: An integer representing the unique identifier for the target chat.
        text: A string representing the text message to be sent.

    Returns:
        A dictionary containing the response data from the API.

    Raises:
        None
    """
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=data)
    return response.json()


def resp_help(chat_id: int) -> None:
    """
    Sends a help message to the user, providing information on the available commands.

    Args:
        chat_id: An integer representing the unique identifier for the target chat.

    Returns:
        None

    Raises:
        None
    """
    help_message = "This is a chatbot that helps to find books!\n"
    help_message += "/list: List all books\n"
    help_message += "/add <title>|<author>|<year>|<ISBN>: Add a new book to the database\n"
    help_message += "/remove <ISBN>: Remove a book by ISBN\n"
    help_message += "/search <keywords>: Search books by keywords\n"
    help_message += "/help: Display this help message\n"
    send_message(chat_id, help_message)


def resp_add_book(chat_id: int, params: list) -> None:
    """
    Adds a new book to the book management system.

    Args:
        chat_id: An integer representing the unique identifier for the target chat.
        params: A list containing the book details: title, author, year, and ISBN.

    Returns:
        None

    Raises:
        None
    """
    if len(params) == 4:
        title, author, year, isbn = params
        if bookManagement.add_book(title, author, year, isbn):
            send_message(chat_id, 'Book added success!')
        else:
            send_message(chat_id, 'Book added failed!')
    else:
        send_message(chat_id, 'Invalid parameters')


def resp_remove_book(chat_id: int, params: list) -> None:
    """
    Removes a book from the book management system.

    Args:
        chat_id: An integer representing the unique identifier for the target chat.
        params: A list containing the ISBN of the book to be removed.

    Returns:
        None

    Raises:
        None
    """
    if len(params) == 1:
        isbn = params[0]
        if bookManagement.delete_book(isbn):
            send_message(chat_id, 'Book removed success!')
        else:
            send_message(chat_id, 'Book removed failed!')
    else:
        send_message(chat_id, 'Invalid parameters')


def resp_search_book(chat_id: int, params: list) -> None:
    """
    Searches for books in the book management system using keywords.

    Args:
        chat_id: An integer representing the unique identifier for the target chat.
        params: A list containing the keywords to search for.

    Returns:
        None

    Raises:
        None
    """
    if len(params) == 1:
        keywords = params[0]
        result = bookManagement.search_books(keywords)
        resp_str_list = []
        num = 1
        for item in result:
            isbn = item['isbn']
            title = item['title']
            author = item['author']
            publish_year = item['publish_year']
            resp_str_list.append(f'#{num}: {isbn} - {title} - {author} - {publish_year}')
            num += 1
        send_message(chat_id, '\n'.join(resp_str_list))
    else:
        send_message(chat_id, 'Invalid parameters')


def resp_list_book(chat_id: int):
    """
    This function handles the list book command. It takes a chat ID as a parameter and uses the `get_all_books` method of the `bookManagement` object to retrieve all books from the database. It then formats the book information for each book into a string and adds it to a response string list. Finally, it sends the response string list to the user using the `send_message` function.

    Args:
        chat_id (int): The ID of the chat with the user.

    Returns:
        None
    """
    result = bookManagement.get_all_books()
    resp_str_list = []
    num = 1
    for item in result:
        isbn = item['isbn']
        title = item['title']
        author = item['author']
        publish_year = item['publish_year']
        resp_str_list.append(f'#{num}: {isbn} - {title} - {author} - {publish_year}')
        num += 1
    send_message(chat_id, '\n'.join(resp_str_list))


def handle_message(data):
    '''
    Handle incoming messages and routes them to corresponding response functions.

    Args:
    - data: A dictionary representing the incoming message data.

    Returns:
    - None
    '''
    try:
        chat_id = data['message']['chat']['id']
        message_text = data['message']['text']

        if message_text.startswith('/help'):
            resp_help(chat_id)
        elif message_text.startswith('/add '):
            params = message_text[len('/add '):].strip().split('|')
            resp_add_book(chat_id, params)
        elif message_text.startswith('/remove '):
            params = message_text[len('/remove '):].strip().split('|')
            resp_remove_book(chat_id, params)
        elif message_text.startswith('/search '):
            params = message_text[len('/search '):].strip().split('|')
            resp_search_book(chat_id, params)
        elif message_text.startswith('/list'):
            resp_list_book(chat_id)
        else:
            send_message(chat_id, "Sorry. I don't known what you mean. \nYou can type /help to get help messages.")
    except:
        pass


def get_updates(offset=None):
    '''
    Receive update messages from telegram server
    Args:
        - offset: the next chat id received from the telegram server
    Returns:
        - None
    '''
    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()


def main():
    '''
    The main program
    '''
    offset = None
    print('ChatBot started')
    while True:
        data = get_updates(offset)
        if len(data['result']) > 0:
            offset = data['result'][-1]['update_id'] + 1
            messages = data['result']
            for msg in messages:
                handle_message(msg)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
