BOOK_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": "Search books in library",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "genre": {"type": "string"},
                }
            }
        }
    }
]