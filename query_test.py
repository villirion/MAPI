import unittest
from query import pageExist, chapterExist, newChapter, isValid
from error import ErrorNotFound, ErrorInvalidPayload

class TestChapterExist(unittest.TestCase):
    def test_chapterExist_error(self):
        _, err = chapterExist("https://www.google.com/","216")
        self.assertIsInstance(err, ErrorInvalidPayload)

    def test_chapterExist_success_lumitoon(self):
        result, err = chapterExist("https://lumitoon.com/series/1706860801-heavenly-demon-chronicles/","226")
        self.assertEqual(err, None)
        self.assertTrue(result)

    def test_chapterExist_success_flamecomics(self):
        result, err = chapterExist("https://flamecomics.com/series/omniscient-readers-viewpoint/","198")
        self.assertEqual(err, None)
        self.assertTrue(result)

    def test_chapterExist_success_mangaclash(self):
        result, err = chapterExist("https://mangaclash.com/manga/infinite-level-up-in-murim/","182")
        self.assertEqual(err, None)
        self.assertTrue(result)

    def test_chapterExist_success_manga4life(self):
        result, err = chapterExist("https://manga4life.com/manga/Masters-of-Lightning-Knives","173")
        self.assertEqual(err, None)
        self.assertTrue(result)

    def test_chapterExist_success_asuratoon(self):
        result, err = chapterExist("https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/","154")
        self.assertEqual(err, None)
        self.assertTrue(result)

    def test_chapterExist_success_reaperscans(self):
        result, err = chapterExist("https://reaperscans.com/comics/4073-overgeared","216")
        self.assertEqual(err, None)
        self.assertTrue(result)


class TestNewChapter(unittest.TestCase):
    def test_newChapter_invalid_url(self):
        _, err = newChapter("broken link",216)
        self.assertIsInstance(err, ErrorInvalidPayload)

    def test_newChapter_new_chapter_available(self):
        result, err = newChapter("https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/",150)
        self.assertEqual(err, None)
        self.assertNotEqual(result, 0)


class TestPageExist(unittest.TestCase):
    def test_pageExist_error(self):
        result = pageExist("test.com")
        self.assertFalse(result)

    def test_pageExist_success(self):
        result = pageExist("https://www.google.com/")
        self.assertTrue(result)

class TestIsValid(unittest.TestCase):
    def test_isValid_error_not_a_site(self):
        result = isValid("test.com", 200)
        self.assertFalse(result)

    def test_isValid_error_unsupported_site(self):
        result = isValid("https://www.google.com/", 200)
        self.assertFalse(result)

    def test_isValid_success(self):
        result = isValid("https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/",150)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()