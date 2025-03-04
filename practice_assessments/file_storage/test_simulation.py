import unittest
from simulation import simulate_coding_framework


class TestSimulateCodingFramework(unittest.TestCase):

    def setUp(self):
        self.test_data_1 = [
            ["FILE_UPLOAD", "Cars.txt", "200kb"],
            ["FILE_GET", "Cars.txt"],
            ["FILE_COPY", "Cars.txt", "Cars2.txt"],
            ["FILE_GET", "Cars2.txt"],
        ]
        self.test_data_2 = [
            ["FILE_UPLOAD", "Foo.txt", "100kb"],
            ["FILE_UPLOAD", "Bar.csv", "200kb"],
            ["FILE_UPLOAD", "Baz.pdf", "300kb"],
            ["FILE_UPLOAD", "Baa.pdf", "300kb"],
            ["FILE_SEARCH", "Ba"],
        ]
        self.test_data_3 = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Python.txt", "150kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "150kb", 3600],
            ["FILE_GET_AT", "2021-07-01T13:00:01", "Python.txt"],
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "Python.txt", "PythonCopy.txt"],
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Py"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Expired.txt", "100kb", 1],
            ["FILE_GET_AT", "2021-07-01T12:00:02", "Expired.txt"],
            [
                "FILE_COPY_AT",
                "2021-07-01T12:00:00",
                "CodeSignal.txt",
                "CodeSignalCopy.txt",
            ],
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Code"],
        ]
        self.test_data_4 = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Initial.txt", "100kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:05:00", "Update1.txt", "150kb", 3600],
            ["FILE_GET_AT", "2021-07-01T12:10:00", "Initial.txt"],
            ["FILE_COPY_AT", "2021-07-01T12:15:00", "Update1.txt", "Update1Copy.txt"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:20:00", "Update2.txt", "200kb", 1800],
            ["ROLLBACK", "2021-07-01T12:10:00"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Update1.txt"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Initial.txt"],
            ["FILE_SEARCH_AT", "2021-07-01T12:25:00", "Up"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Update2.txt"],
        ]

    def test_group_1(self):
        output = simulate_coding_framework(self.test_data_1)
        self.assertEqual(
            output,
            [
                "uploaded Cars.txt",
                "200kb",
                "copied Cars.txt to Cars2.txt",
                "200kb",
            ],
        )

    def test_group_2(self):
        output = simulate_coding_framework(self.test_data_2)
        self.assertEqual(
            output,
            [
                "uploaded Foo.txt",
                "uploaded Bar.csv",
                "uploaded Baz.pdf",
                "uploaded Baa.pdf",
                ["Baa.pdf", "Baz.pdf", "Bar.csv"],
            ],
        )

    def test_group_3(self):
        output = simulate_coding_framework(self.test_data_3)
        self.assertEqual(
            output,
            [
                "uploaded Python.txt",
                "uploaded CodeSignal.txt",
                "150kb",
                "copied Python.txt to PythonCopy.txt",
                ["Python.txt", "PythonCopy.txt"],
                "uploaded Expired.txt",
                None,
                "copied CodeSignal.txt to CodeSignalCopy.txt",
                ["CodeSignal.txt", "CodeSignalCopy.txt"],
            ],
        )

    def test_group_4(self):
        output = simulate_coding_framework(self.test_data_4)
        self.assertEqual(
            output,
            [
                "uploaded Initial.txt",
                "uploaded Update1.txt",
                "100kb",
                "copied Update1.txt to Update1Copy.txt",
                "uploaded Update2.txt",
                "rollback to 2021-07-01T12:10:00",
                "150kb",
                "100kb",
                ["Update1.txt"],
                None,
            ],
        )


if __name__ == "__main__":
    unittest.main()
