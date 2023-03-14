# BookGPT (to improve my code skills)

I came up with this idea by reading "how to read a book".

I hope AI can follow some of the rules and apply methodology to read a novel using sequential timeline.

This project is for **fun**.

I used this project to improve my code skills to build infrastructure from scratch.

These classes are built with detailed logging and error checking system (where I want to improve for my code skills)



## Book class

Book is a Python class designed to read a book from a text file and split it into chunks of a specified length. Book also has a `get_info()` method that uses a GPT-based chatbot to extract information about the book, such as its title, author, genre, and theme.

### Usage

To use Book, first create an instance of the class and specify the path to the book's text file:

```
pythonCopy code
book = Book("path/to/book.txt")
```

You can then split the book into chunks of a specified length (in words) using the `split_book()` method:

```
pythonCopy code
book_chunks = book.split_book(word_length=1000, start_page=1)
```

By default, `split_book()` splits the book into chunks of 1000 words, starting from the first page. You can specify a different length and starting page by passing values to the `word_length` and `start_page` parameters, respectively.

You can also use the `get_info()` method to extract information about the book:

```
pythonCopy code
book.get_info()
```

This method uses a GPT-based chatbot to extract information about the book, such as its title, author, genre, and theme.

### Configuration

Book reads its configuration from a `config.json` file in the same directory as the `Book` class. The following options are available:

- `logging_file_path`: The file path to use for logging.
- `structure_file_path`: The file path to use for the structure prompts.

### Logging

Book logs its activity to a file specified in the `logging_file_path` option of the `config.json` file. The log file contains information about the book loading and splitting, as well as any errors that occur.



## ChatGPT class

ChatGPT is a Python class designed to facilitate interactions with OpenAI's GPT-based chatbots. This class handles session management and provides a high-level function to send a message and receive a response.

### Usage

To use ChatGPT, first create an instance of the class:

```
pythonCopy code
chatbot = ChatGPT()
```

By default, ChatGPT uses the GPT-3.5 Turbo 0301 model, but you can specify a different model by passing the model name to the `model` parameter:

```
pythonCopy code
chatbot = ChatGPT(model="gpt-3")
```

You can then send a message and receive a response using the `send_message()` method:

```
pythonCopy code
response = chatbot.send_message("Hello, how are you?")
```

By default, `send_message()` returns a string containing the response. However, you can also set the `make_json` parameter to `True` to return the response as a JSON object:

```
pythonCopy code
response_json = chatbot.send_message("Hello, how are you?", make_json=True)
```

You can also specify a custom system message to use instead of the default prompt:

```
pythonCopy code
response = chatbot.send_message("Hello, how are you?", system_message="What can I do for you?")
```

### Configuration

ChatGPT reads its configuration from a `config.json` file in the same directory as the `ChatGPT` class. The following options are available:

- `default_system_prompt`: The default prompt to use if a custom system message is not specified.
- `model`: The name of the GPT-based chatbot model to use.
- `prompt_failure_times`: The maximum number of times to retry getting a response as JSON.
- `log_conversation`: Whether to log the conversation to a file.
- `conversation_file_path`: The file path to use for logging the conversation.

### Logging

ChatGPT can log conversation history to a file if the `log_conversation` option is set to `True`. The conversation is logged in the following format:

```
makefileCopy code
Conversation: <conversation number>
System: <system message>
User: <user message>
Response: <response message>
Usage: <total number of tokens used>
```



Already discarded. Because I realize langchain is more useful to build the project.