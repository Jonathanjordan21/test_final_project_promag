from src.components.extract import scrape_review, scrape_toko, scrape, scrape_review_toko
import unittest

class TestScrape(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestScrape, self).__init__(*args, **kwargs)
        self.link = "https://www.tokopedia.com/distrilapid/laptop-asus-vivobook-14-a416mao-celeron-n4020-ram-8gb-512gb-ssd-ohs-4gb-silver-256gb-afe06?extParam=ivf%3Dtrue%26src%3Dsearch"
        self.produk = "laptop"
        self.jumlah_halaman = 3
        self.nama_toko = "unilever"
    def test_scrape(self):
        data = scrape.run(self.produk, self.jumlah_halaman, True)
        self.assertGreater(len(data), 6)
    def test_scrape_review(self):
        data = scrape_review.run(self.link, self.jumlah_halaman, True)
        self.assertGreater(len(data), 6)
    def test_scrape_toko(self):
        data = scrape_toko.run(self.nama_toko, self.jumlah_halaman, True)
        self.assertGreater(len(data), 6)
    def test_scrape_review_toko(self):
        data = scrape_review_toko.run(self.nama_toko, self.jumlah_halaman,True)
        self.assertGreater(len(data), 6)


if __name__ == '__main__':
    unittest.main()