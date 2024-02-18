import unittest
from query import check_page_existence, get_chapter_url, get_status, check_valid

class TestGetChapterUrl(unittest.TestCase):
    def test_get_chapter_url_success_lumitoon(self):
        result = get_chapter_url("https://lumitoon.com/series/1706860801-heavenly-demon-chronicles/","226")
        self.assertEqual(result, "https://lumitoon.com/the-chronicles-of-heavenly-demon-chapter-226/")

    def test_get_chapter_url_success_flamecomics(self):
        result = get_chapter_url("https://flamecomics.com/series/omniscient-readers-viewpoint/","198")
        self.assertEqual(result, "https://flamecomics.com/omniscient-readers-viewpoint-chapter-198/")

    def test_get_chapter_url_success_mangaclash(self):
        result = get_chapter_url("https://mangaclash.com/manga/infinite-level-up-in-murim/","182")
        self.assertEqual(result, "https://mangaclash.com/manga/infinite-level-up-in-murim/chapter-182/")

    def test_get_chapter_url_success_manga4life(self):
        result = get_chapter_url("https://manga4life.com/manga/Masters-of-Lightning-Knives","173")
        self.assertEqual(result, "https://manga4life.com/read-online/Masters-of-Lightning-Knives-chapter-173.html")

    def test_get_chapter_url_success_asuratoon(self):
        result = get_chapter_url("https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/","154")
        self.assertEqual(result, "https://asuratoon.com/5588556462-the-max-level-hero-has-returned-chapter-154/")

    def test_get_chapter_url_success_reaperscans(self):
        result = get_chapter_url("https://reaperscans.com/comics/4073-overgeared","216")
        self.assertEqual(result, "https://reaperscans.com/comics/4073-overgeared/chapters/43419163-chapter-216")

    def test_get_chapter_url_error(self):
        result = get_chapter_url("https://www.google.com/","216")
        self.assertEqual(result, "Unsupported site")


class TestGetStatus(unittest.TestCase):
    def test_get_status_broken_link(self):
        result = get_status("broken link",216)
        self.assertEqual(result, "Link broken")

    def test_get_status_new_chapter_available(self):
        result = get_status("https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/",150)
        self.assertEqual(result, "New chapter available")

    def test_get_status_up_to_date(self):
        result = get_status("https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/",10000)
        self.assertEqual(result, "Up to date")

    def test_get_status_error(self):
        result = get_status("https://www.google.com/",10000)
        self.assertEqual(result, "Unsupported site")

class TestCheckPageExistence(unittest.TestCase):
    def test_check_page_existence_error(self):
        result = check_page_existence("test.com")
        self.assertFalse(result)

    def test_check_page_existence_success(self):
        result = check_page_existence("https://www.google.com/")
        self.assertTrue(result)

class TestCheckValid(unittest.TestCase):
    def test_check_valid_error_not_a_site(self):
        result = check_valid("test.com", 200)
        self.assertFalse(result)

    def test_check_valid_error_unsupported_site(self):
        result = check_valid("https://www.google.com/", 200)
        self.assertFalse(result)

    def test_check_valid_success(self):
        result = check_valid("https://asuratoon.com/manga/5588556462-the-max-level-hero-has-returned/",150)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()