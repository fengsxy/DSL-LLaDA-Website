import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WebsiteTests(unittest.TestCase):
    def test_demo_page_is_static_and_pages_safe(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn('<h1 id="page-title">DSL-LLaDA</h1>', html)
        self.assertIn('const TRACE_URL = "demo/traces/showcase.json"', html)
        self.assertIn('href="about.html"', html)
        self.assertNotIn('href="/about.html"', html)
        self.assertNotIn('href="/generate"', html)
        self.assertNotIn("Final output", html)

    def test_about_page_is_separate_and_uses_relative_links(self):
        demo_html = (ROOT / "index.html").read_text(encoding="utf-8")
        about_html = (ROOT / "about.html").read_text(encoding="utf-8")

        self.assertNotIn("Delay the hard decision.", demo_html)
        self.assertIn("Delay the hard decision.", about_html)
        self.assertIn("What the replay supports.", about_html)
        self.assertIn('href="index.html"', about_html)
        self.assertNotIn('href="/"', about_html)

    def test_showcase_contains_matched_real_traces(self):
        showcase = json.loads(
            (ROOT / "demo" / "traces" / "showcase.json").read_text(
                encoding="utf-8"
            )
        )
        cases = showcase["cases"]

        self.assertEqual(
            [case["task"] for case in cases],
            ["xsum", "travel", "aeslc"],
        )
        self.assertEqual(showcase["metadata"]["protocols"]["xsum-6"]["nfe"], 8)
        self.assertEqual(
            showcase["metadata"]["protocols"]["travel-0"]["nfe"],
            32,
        )

        for case in cases:
            dsl_run = case["dsl"]["run"]
            llada_run = case["llada"]["run"]
            self.assertEqual(dsl_run["nfe"], llada_run["nfe"])
            self.assertEqual(
                dsl_run["generation_tokens"],
                llada_run["generation_tokens"],
            )
            self.assertGreater(len(case["dsl"]["trace"]), 1)
            self.assertGreater(len(case["llada"]["trace"]), 1)
            self.assertTrue(case["dsl"]["output"])
            self.assertTrue(case["llada"]["output"])

    def test_release_excludes_large_or_runtime_only_artifacts(self):
        self.assertFalse(
            (ROOT / "demo" / "traces" / "candidate_scores.json").exists()
        )
        self.assertFalse((ROOT / "checkpoints").exists())
        self.assertFalse((ROOT / "demo" / "app.py").exists())


if __name__ == "__main__":
    unittest.main()
