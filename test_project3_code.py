import unittest
from project3_code import SeleniumProjectChrome

class TestSeleniumProjectChrome(unittest.TestCase):
    def setUp(self):
        self.project = SeleniumProjectChrome("https://www.google.com")
        self.project.open_website()

    def test_search(self):
        self.project.perform_search("Selenium test")
        search_results = self.project.get_search_results()
        self.assertTrue(len(search_results) > 0, "Search results should not be empty.")

    def tearDown(self):
        self.project.close_browser()

if __name__ == "__main__":
    unittest.main()
