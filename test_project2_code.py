import unittest
from project2_code import login_to_local_page

class TestProject2Code(unittest.TestCase):

    def test_login_to_local_page_success(self):
        login_to_local_page("user123", "pass456")  # Adjust based on your actual test

    def test_login_to_local_page_failure(self):
        login_to_local_page("invalid_user", "invalid_pass")  # Adjust based on your actual test

if __name__ == '__main__':
    unittest.main()
