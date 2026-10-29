import hashlib
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.cell import WriteOnlyCell

from scripts.merge_social_datasets import COLUMNS, merge


class MergeTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)

    def source(self, name, rows):
        path = self.root / (name + ".xlsx")
        book = Workbook()
        sheet = book.active
        sheet.title = "Data"
        sheet.append(COLUMNS)
        for platform, kind, url, text in rows:
            values = [
                platform,
                kind,
                "Title",
                None,
                "pasti",
                None,
                "pasti",
                text,
                url,
                False,
            ]
            safe = []
            for value in values:
                cell = WriteOnlyCell(sheet, value=value)
                if isinstance(value, str):
                    cell.data_type = "s"
                safe.append(cell)
            sheet.append(safe)
        book.save(path)
        return path

    def run_merge(self, sources):
        return merge(sources, self.root / "combined", self.root / "provenance.json")

    def test_merge_preserves_identical_text_distinct_ids_and_formula_like_text(self):
        a = self.source(
            "a",
            [
                (
                    "youtube",
                    "video",
                    "https://www.youtube.com/watch?v=videoA",
                    "Root A",
                ),
                (
                    "youtube",
                    "comment",
                    "https://www.youtube.com/watch?v=videoA&lc=c1",
                    "=same text",
                ),
            ],
        )
        b = self.source(
            "b",
            [
                ("reddit", "post", "https://www.reddit.com/comments/abc/", "Root B"),
                (
                    "reddit",
                    "reply",
                    "https://www.reddit.com/comments/abc/_/c2/",
                    "=same text",
                ),
            ],
        )
        hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (a, b)]
        result = self.run_merge([a, b])
        self.assertEqual(
            (result["rows"], result["roots"], result["comments"]), (4, 2, 2)
        )
        self.assertEqual([s["sha256"] for s in result["source_workbooks"]], hashes)
        self.assertEqual(
            [s["first_excel_row"] for s in result["source_workbooks"]], [2, 4]
        )
        self.assertEqual(
            [hashlib.sha256(p.read_bytes()).hexdigest() for p in (a, b)], hashes
        )
        book = load_workbook(result["output"], read_only=True, data_only=False)
        cells = list(book["Data"].iter_rows())
        self.assertEqual(
            (cells[2][7].value, cells[2][7].data_type), ("=same text", "s")
        )
        self.assertEqual(cells[4][7].value, "=same text")
        book.close()

    def test_same_native_id_different_kind_is_rejected_without_publication(self):
        a = self.source(
            "a",
            [
                ("reddit", "post", "https://www.reddit.com/comments/abc/", "root"),
                (
                    "reddit",
                    "comment",
                    "https://www.reddit.com/comments/abc/_/c1/",
                    "text",
                ),
            ],
        )
        b = self.source(
            "b",
            [
                (
                    "reddit",
                    "reply",
                    "https://www.reddit.com/comments/abc/_/c1/",
                    "changed",
                )
            ],
        )
        with self.assertRaisesRegex(ValueError, "Duplicate native content"):
            self.run_merge([a, b])
        self.assertFalse((self.root / "combined").exists())

    def test_orphan_comment_is_rejected(self):
        a = self.source(
            "a",
            [
                (
                    "youtube",
                    "comment",
                    "https://www.youtube.com/watch?v=videoA&lc=c1",
                    "orphan",
                )
            ],
        )
        with self.assertRaisesRegex(ValueError, "Orphan comments"):
            self.run_merge([a])


if __name__ == "__main__":
    unittest.main()
