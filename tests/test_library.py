import pytest
from src.library import LibraryManager, Book


class TestLibraryManager:
    """测试图书管理器功能"""

    @pytest.fixture
    def library(self):
        """创建一个新的图书馆管理器实例"""
        return LibraryManager()

    def test_add_book_success(self, library):
        """测试成功添加图书"""
        result = library.add_book("Python编程", "张三", "978-7-111-12345-6")
        assert result is True
        books = library.list_all_books()
        assert len(books) == 1
        assert books[0].title == "Python编程"
        assert books[0].author == "张三"
        assert books[0].isbn == "978-7-111-12345-6"

    def test_add_book_duplicate_isbn(self, library):
        """测试添加重复ISBN的图书应失败"""
        library.add_book("Python编程", "张三", "978-7-111-12345-6")
        result = library.add_book("Java编程", "李四", "978-7-111-12345-6")
        assert result is False
        books = library.list_all_books()
        assert len(books) == 1
        assert books[0].title == "Python编程"

    def test_add_book_empty_fields_raises_error(self, library):
        """测试添加空字段应抛出异常"""
        with pytest.raises(ValueError):
            library.add_book("", "张三", "978-7-111-12345-6")
        
        with pytest.raises(ValueError):
            library.add_book("Python编程", "", "978-7-111-12345-6")
        
        with pytest.raises(ValueError):
            library.add_book("Python编程", "张三", "")

    def test_get_book_by_isbn_success(self, library):
        """测试通过ISBN成功获取图书"""
        library.add_book("Python编程", "张三", "978-7-111-12345-6")
        book = library.get_book_by_isbn("978-7-111-12345-6")
        assert isinstance(book, Book)
        assert book.title == "Python编程"

    def test_get_book_by_isbn_not_found(self, library):
        """测试通过不存在的ISBN获取图书应抛出KeyError"""
        with pytest.raises(KeyError):
            library.get_book_by_isbn("978-0-000-00000-0")

    def test_search_books_by_title_partial_match(self, library):
        """测试按书名部分匹配查询"""
        library.add_book("Python编程入门", "张三", "978-7-111-12345-6")
        library.add_book("Java编程", "李四", "978-7-111-12345-7")
        library.add_book("C++编程", "王五", "978-7-111-12345-8")
        
        results = library.search_books_by_title("编程")
        assert len(results) == 3
        
        results = library.search_books_by_title("Python")
        assert len(results) == 1
        assert results[0].title == "Python编程入门"

    def test_search_books_by_title_case_insensitive(self, library):
        """测试搜索不区分大小写"""
        library.add_book("Python编程", "张三", "978-7-111-12345-6")
        
        results_upper = library.search_books_by_title("PYTHON")
        results_lower = library.search_books_by_title("python")
        
        assert len(results_upper) == 1
        assert len(results_lower) == 1
        assert results_upper[0].title == results_lower[0].title

    def test_search_books_by_title_no_match(self, library):
        """测试无匹配结果时返回空列表"""
        library.add_book("Python编程", "张三", "978-7-111-12345-6")
        results = library.search_books_by_title("JavaScript")
        assert results == []

    def test_search_books_by_title_empty_string(self, library):
        """测试搜索空字符串返回空列表"""
        library.add_book("Python编程", "张三", "978-7-111-12345-6")
        results = library.search_books_by_title("")
        assert results == []

    def test_delete_book_success(self, library):
        """测试成功删除图书"""
        library.add_book("Python编程", "张三", "978-7-111-12345-6")
        result = library.delete_book("978-7-111-12345-6")
        assert result is True
        books = library.list_all_books()
        assert len(books) == 0

    def test_delete_book_not_found(self, library):
        """测试删除不存在的图书返回False"""
        result = library.delete_book("978-0-000-00000-0")
        assert result is False
        books = library.list_all_books()
        assert len(books) == 0

    def test_list_all_books_initially_empty(self, library):
        """测试初始状态下图书列表为空"""
        books = library.list_all_books()
        assert books == []

    def test_list_all_books_multiple_books(self, library):
        """测试列出多本图书"""
        library.add_book("Python编程", "张三", "978-7-111-12345-6")
        library.add_book("Java编程", "李四", "978-7-111-12345-7")
        library.add_book("C++编程", "王五", "978-7-111-12345-8")
        
        books = library.list_all_books()
        assert len(books) == 3
        
        titles = [book.title for book in books]
        assert "Python编程" in titles
        assert "Java编程" in titles
        assert "C++编程" in titles

    def test_book_equality(self):
        """测试图书相等性比较"""
        book1 = Book("Python编程", "张三", "978-7-111-12345-6")
        book2 = Book("Python编程", "张三", "978-7-111-12345-6")
        book3 = Book("Java编程", "李四", "978-7-111-12345-7")
        
        assert book1 == book2
        assert book1 != book3

    def test_book_repr(self):
        """测试图书字符串表示"""
        book = Book("Python编程", "张三", "978-7-111-12345-6")
        repr_str = repr(book)
        assert "Python编程" in repr_str
        assert "张三" in repr_str
        assert "978-7-111-12345-6" in repr_str