import unittest
from persistence import setupCSV, List, Get, Post, updateCSV, Update, Delete
import pandas as pd
from pandas.testing import assert_frame_equal
from datetime import datetime

class TestSetupCSV(unittest.TestCase):
    def test_setupCSV_success(self):
        result = setupCSV("test.csv")
        self.assertIsNotNone(result)

class TestUpdateCSV(unittest.TestCase):
    def test_updateCSV_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2'],
            'SITE': ['Site1', 'Site2'],
            'CHAPTER': [1, 22],
            'STATUS': ['Link broken', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        expected_df = setupCSV("test.csv")
        assert_frame_equal(df, expected_df)

class TestList(unittest.TestCase):
    def test_list_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2'],
            'SITE': ['Site1', 'Site2'],
            'CHAPTER': [1, 22],
            'STATUS': ['Link broken', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        expected_result = [
            {'TITLE': 'Title1', 'SITE': 'Site1', 'CHAPTER': 1, 'STATUS': 'Link broken', 'LAST_UPDATE': '2023-02-18'},
            {'TITLE': 'Title2', 'SITE': 'Site2', 'CHAPTER': 22, 'STATUS': 'Link broken', 'LAST_UPDATE': '2024-02-02'}
        ]

        result = List("test.csv")
        self.assertEqual(result, expected_result)

class TestGet(unittest.TestCase):
    def test_get_error(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        result = Get("test.csv", 'Title8')
        self.assertEqual(result, ({'ERROR': 'not found'}, 404))

    def test_get_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        result = Get("test.csv", 'Title2')
        self.assertEqual(result, ({'TITLE': 'Title2', 'SITE': 'Site2', 'CHAPTER': 2, 'STATUS': 'Up to date', 'LAST_UPDATE': '2023-02-18'}, 200))

class TestPost(unittest.TestCase):
    def test_post_error(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        data = {'TITLE': 'Title4'}

        result = Post("test.csv", data)
        self.assertEqual(result, ({'ERROR': 'Invalid data format'}, 400))

    def test_post_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        date = datetime.now().date()

        expected_df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3', 'Title4'],
            'SITE': ['Site1', 'Site2', 'Site3', 'https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/'],
            'CHAPTER': [54, 2, 6, 8],
            'STATUS': ['Link broken', 'Up to date', 'Link broken', 'New chapter available'],
        })

        data = {
            'TITLE': 'Title4',
            'SITE': 'https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/',
            'CHAPTER': 8
        }

        result = Post("test.csv", data)
        self.assertEqual(result, ({'TITLE': 'Title4', 'SITE': 'https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/', 'CHAPTER': 8, 'STATUS': 'New chapter available', 'LAST_UPDATE': date}, 200))

        result_df = setupCSV("test.csv")
        result_df = result_df.drop(columns=['LAST_UPDATE'])
        assert_frame_equal(result_df, expected_df)

class TestUpdate(unittest.TestCase):
    def test_update_error_400(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        data = {'TITLE': 'Title2'}

        result = Update("test.csv", data)
        self.assertEqual(result, ({'ERROR': 'Invalid data format'}, 400))

    def test_update_error_404(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        data = {
            'TITLE': 'Title4',
            'SITE': 'Site4',
            'CHAPTER': 'Chapter5',
        }

        result = Update("test.csv", data)
        self.assertEqual(result, ({'ERROR': 'not found'}, 404))

    def test_update_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        date = datetime.now().date()

        expected_df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/', 'Site3'],
            'CHAPTER': [54, 5, 6],
            'STATUS': ['Link broken', 'New chapter available', 'Link broken'],
        })

        data = {
            'TITLE': 'Title2',
            'SITE': 'https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/',
            'CHAPTER': 5,
        }

        result = Update("test.csv", data)
        self.assertEqual(result, ({'TITLE': 'Title2', 'SITE': 'https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/', 'CHAPTER': 5, 'STATUS': 'New chapter available', 'LAST_UPDATE': date}, 200))

        result_df = setupCSV("test.csv")
        result_df = result_df.drop(columns=['LAST_UPDATE'])
        assert_frame_equal(result_df, expected_df)

class TestDelete(unittest.TestCase):
    def test_delete_error_404(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        data = {'TITLE': 'Title5'}

        result = Delete("test.csv", data)
        self.assertEqual(result, ({'ERROR': 'not found'}, 404))

    def test_delete_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': [54, 2, 6],
            'STATUS': ['Link broken', 'Up to date', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2023-02-18', '2024-02-02']
        })

        updateCSV(df, "test.csv")

        expected_df = pd.DataFrame({
            'TITLE': ['Title1', 'Title3'],
            'SITE': ['Site1', 'Site3'],
            'CHAPTER': [54, 6],
            'STATUS': ['Link broken', 'Link broken'],
            'LAST_UPDATE': ['2023-02-18', '2024-02-02']
        })

        data = {'TITLE': 'Title2'}

        result = Delete("test.csv", data)
        self.assertEqual(result, ({}, 200))

        result_df = setupCSV("test.csv")
        assert_frame_equal(result_df, expected_df)

if __name__ == '__main__':
    unittest.main()