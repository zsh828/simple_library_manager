class Book:
    """图书类，表示一本具体的书"""
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn

    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"


class LibraryManager:
    """图书管理器，负责管理图书的增删改查"""
    
    def __init__(self):
        # 使用字典存储图书，key为ISBN，value为Book对象
        self._books = {}

    def add_book(self, title: str, author: str, isbn: str) -> bool:
        """
        添加图书
        
        Args:
            title: 书名
            author: 作者
            isbn: ISBN号
            
        Returns:
            bool: 如果添加成功（ISBN不存在）返回True，如果ISBN已存在返回False
        """
        if not isbn or not title or not author:
            raise ValueError("Title, author, and ISBN cannot be empty")
        
        if isbn in self._books:
            return False
        
        book = Book(title=title, author=author, isbn=isbn)
        self._books[isbn] = book
        return True

    def get_book_by_isbn(self, isbn: str) -> Book:
        """
        根据ISBN查询图书
        
        Args:
            isbn: ISBN号
            
        Returns:
            Book: 找到的图书对象
            
        Raises:
            KeyError: 如果未找到该ISBN对应的图书
        """
        if isbn not in self._books:
            raise KeyError(f"Book with ISBN {isbn} not found")
        return self._books[isbn]

    def search_books_by_title(self, title: str) -> list:
        """
        按书名模糊查询图书
        
        Args:
            title: 书名关键字
            
        Returns:
            list: 包含匹配标题的图书列表
        """
        if not title:
            return []
        
        results = []
        for book in self._books.values():
            if title.lower() in book.title.lower():
                results.append(book)
        return results

    def delete_book(self, isbn: str) -> bool:
        """
        删除图书
        
        Args:
            isbn: ISBN号
            
        Returns:
            bool: 如果删除成功返回True，如果ISBN不存在返回False
        """
        if isbn in self._books:
            del self._books[isbn]
            return True
        return False

    def list_all_books(self) -> list:
        """
        列出所有图书
        
        Returns:
            list: 包含所有图书对象的列表
        """
        return list(self._books.values())