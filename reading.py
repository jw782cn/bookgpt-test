# reading is a class to read the book
import utils
import os
from chatgpt import ChatGPT
import json

class Book():
    def __init__(self, book_txt_path) -> None:
        self._get_config()
        self.book_txt_path = book_txt_path
        self.book = None
        self.word_length = 1000
        self.book_title = None
        self.book_author = None
        self.book_description = None
        self.chunks = None
        self.book_theme = None
        self.book_genre = None
        self.chatgpt = ChatGPT(self.logger)
    
    # get information about the book
    def get_info(self):
        # feed in the first chunk to get the information
        self.logger.info(f'getting book info')
        if self.chunks is None:
            return
        prompt = self.structure_prompts["book_info"]
        self.logger.info(f'prompt: {prompt}')
        # make_json=True to get json response
        info = self.chatgpt.send_message(user_message=self.chunks[0], system_message=prompt, make_json=True)
        self.logger.info(f'book info: {info}')
        self.book_title = info["title"]
        self.book_author = info["author"]
        self.book_genre = info["genre"]
        self.book_theme = info["theme"]
    
    # split book into chunks
    # TODO: change to more robust method
    def split_book(self, word_length=1000, start_page=1):
        if self.book is None:
            self._load_book()
        if self.book is None:
            return None
        if word_length != self.word_length:
            self.word_lenth = word_length
        book = self.book
        book_chunks = utils.text_to_chunks(book, word_length=word_length, start_page=start_page)
        self.chunks = book_chunks
        self.logger.info(f'book split into {len(book_chunks)} chunks')
        return book_chunks
    
    def _get_config(self):
        config = utils.json_read("config.json")
        self.logging_file_path = config["logging_file_path"]
        self.logger = utils.get_logger(self.logging_file_path)
        self.structure_file_path = config["structure_file_path"]
        self.structure_prompts = utils.json_read(self.structure_file_path)
        # print(self.structure_prompts)
        
    # load book from txt file
    def _load_book(self):
        book = utils.file_read_from_txt(self.book_txt_path)
        self.book = book
        self.logger.info(f'book loaded from {self.book_txt_path}')
        return self.book
    
    
    