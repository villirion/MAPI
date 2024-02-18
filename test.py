import unittest
from persistence import setupCSV, List, Get, Post, updateCSV, Update, Delete
from query import check_page_existence, check_all_page_existence, check_all_new_chapter, get_last_chapter_url
import pandas as pd
from pandas.testing import assert_frame_equal

class TestSetupCSV(unittest.TestCase):
    def test_setupCSV_success(self):
        result = setupCSV("test.csv")
        self.assertIsNotNone(result)

class TestUpdateCSV(unittest.TestCase):
    def test_updateCSV_success(self):
        expected_df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(expected_df, "test.csv")

        df = pd.read_csv("test.csv")

        assert_frame_equal(df, expected_df)

class TestList(unittest.TestCase):
    def test_list_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2'],
            'SITE': ['Site1', 'Site2'],
            'CHAPTER': ['Chapter1', 'Chapter2']
        })

        updateCSV(df, "test.csv")

        expected_result = [
            {'TITLE': 'Title1', 'SITE': 'Site1', 'CHAPTER': 'Chapter1'},
            {'TITLE': 'Title2', 'SITE': 'Site2', 'CHAPTER': 'Chapter2'}
        ]

        result = List("test.csv")
        self.assertEqual(result, expected_result)

class TestGet(unittest.TestCase):
    def test_get_error(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        result = Get("test.csv", 'Title8')
        self.assertEqual(result, ({'ERROR': 'not found'}, 404))

    def test_get_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        result = Get("test.csv", 'Title2')
        self.assertEqual(result, ({'TITLE': 'Title2', 'SITE': 'Site2', 'CHAPTER': 'Chapter2'}, 200))

class TestPost(unittest.TestCase):
    def test_post_error(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        data = {'TITLE': 'Title4'}

        result = Post("test.csv", data)
        self.assertEqual(result, ({'ERROR': 'Invalid data format'}, 400))

    def test_post_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        expected_df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3', 'Title4'],
            'SITE': ['Site1', 'Site2', 'Site3', 'Site4'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3', 'Chapter4']
        })

        data = {
            'TITLE': 'Title4',
            'SITE': 'Site4',
            'CHAPTER': 'Chapter4'
        }

        result = Post("test.csv", data)
        self.assertEqual(result, ({'TITLE': 'Title4', 'SITE': 'Site4', 'CHAPTER': 'Chapter4'}, 200))

        result_df = setupCSV("test.csv")
        assert_frame_equal(result_df, expected_df)

class TestUpdate(unittest.TestCase):
    def test_update_error_400(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        data = {'TITLE': 'Title2'}

        result = Update("test.csv", data)
        self.assertEqual(result, ({'ERROR': 'Invalid data format'}, 400))

    def test_update_error_404(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
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
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        expected_df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site4', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter5', 'Chapter3']
        })

        data = {
            'TITLE': 'Title2',
            'SITE': 'Site4',
            'CHAPTER': 'Chapter5',
        }

        result = Update("test.csv", data)
        self.assertEqual(result, ({'TITLE': 'Title2', 'SITE': 'Site4', 'CHAPTER': 'Chapter5'}, 200))

        result_df = setupCSV("test.csv")
        assert_frame_equal(result_df, expected_df)

class TestDelete(unittest.TestCase):
    def test_delete_error_400(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        data = {'SITE': 'Site2'}

        result = Delete("test.csv", data)
        self.assertEqual(result, ({'ERROR': 'Invalid data format'}, 400))


    def test_delete_error_404(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        data = {'TITLE': 'Title5'}

        result = Delete("test.csv", data)
        self.assertEqual(result, ({'ERROR': 'not found'}, 404))

    def test_delete_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['Site1', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        expected_df = pd.DataFrame({
            'TITLE': ['Title1', 'Title3'],
            'SITE': ['Site1', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter3']
        })

        data = {'TITLE': 'Title2'}

        result = Delete("test.csv", data)
        self.assertEqual(result, ({}, 200))

        result_df = setupCSV("test.csv")
        assert_frame_equal(result_df, expected_df)

class TestCheckPageExistence(unittest.TestCase):
    def test_check_page_existence_error(self):
        result = check_page_existence("test.com")
        self.assertFalse(result)

    def test_check_page_existence_success(self):
        result = check_page_existence("https://www.google.com/")
        self.assertTrue(result)

class TestCheckAllPageExistence(unittest.TestCase):
    def test_check_all_page_existence_success(self):
        df = pd.DataFrame({
            'TITLE': ['Title1', 'Title2', 'Title3'],
            'SITE': ['https://www.google.com/', 'Site2', 'Site3'],
            'CHAPTER': ['Chapter1', 'Chapter2', 'Chapter3']
        })

        updateCSV(df, "test.csv")

        expected_result = [
            {'TITLE': 'Title2', 'SITE': 'Site2', 'CHAPTER': 'Chapter2'},
            {'TITLE': 'Title3', 'SITE': 'Site3', 'CHAPTER': 'Chapter3'}
        ]

        result = check_all_page_existence("test.csv")
        self.assertTrue(result)

class TestGetLastChapterUrl(unittest.TestCase):
    def test_get_last_chapter_url_success_lumitoon(self):
        result = get_last_chapter_url("https://lumitoon.com/series/1706860801-heavenly-demon-chronicles/",226)
        self.assertEqual(result, "https://lumitoon.com/the-chronicles-of-heavenly-demon-chapter-226/")

    def test_get_last_chapter_url_success_flamecomics(self):
        result = get_last_chapter_url("https://flamecomics.com/series/omniscient-readers-viewpoint/",198)
        self.assertEqual(result, "https://flamecomics.com/omniscient-readers-viewpoint-chapter-198/")

    def test_get_last_chapter_url_success_mangaclash(self):
        result = get_last_chapter_url("https://mangaclash.com/manga/infinite-level-up-in-murim/",182)
        self.assertEqual(result, "https://mangaclash.com/manga/infinite-level-up-in-murim/chapter-182/")

    def test_get_last_chapter_url_success_manga4life(self):
        result = get_last_chapter_url("https://manga4life.com/manga/Masters-of-Lightning-Knives",173)
        self.assertEqual(result, "https://manga4life.com/read-online/Masters-of-Lightning-Knives-chapter-173.html")

    def test_get_last_chapter_url_success_asuratoon(self):
        result = get_last_chapter_url("https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/",154)
        self.assertEqual(result, "https://asuratoon.com/5588556462-the-max-level-hero-has-returned-chapter-154/")

    def test_get_last_chapter_url_success_reaperscans(self):
        result = get_last_chapter_url("https://reaperscans.com/comics/4073-overgeared",216)
        self.assertEqual(result, "https://reaperscans.com/comics/4073-overgeared/chapters/43419163-chapter-216")


class TestCheckAllNewChapter(unittest.TestCase):
    def test_check_all_new_chapter_success(self):
        df = pd.DataFrame({
            'TITLE': ['The Heavenly Demon Can’t Live a Normal Life'],
            'SITE': ['https://asuratoon.com/manga/5588556462-the-heavenly-demon-cant-live-a-normal-life/'],
            'CHAPTER': [107]
        })

        updateCSV(df, "test.csv")

        result = check_all_new_chapter("test.csv")
        self.assertEqual(result, [{"TITLE": "The Heavenly Demon Can’t Live a Normal Life", 'SITE': 'https://asuratoon.com/manga/5588556462-the-heavenly-demon-cant-live-a-normal-life/', 'CHAPTER': 107}])

if __name__ == '__main__':
    unittest.main()