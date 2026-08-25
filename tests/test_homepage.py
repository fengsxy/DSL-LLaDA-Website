import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WebsiteTests(unittest.TestCase):
    def test_unified_homepage_is_static_and_pages_safe(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn('<h1 id="page-title">DSL-LLaDA</h1>', html)
        self.assertIn('const TRACE_URL = "demo/traces/showcase.json"', html)
        self.assertIn("Findings of EMNLP 2026", html)
        self.assertIn('id="demo"', html)
        self.assertIn('id="method"', html)
        self.assertIn('id="results"', html)
        self.assertIn('id="ocr"', html)
        self.assertIn('id="scope"', html)
        self.assertIn('id="resources"', html)
        self.assertIn('id="source-dialog"', html)
        self.assertIn('sourceLabel.textContent = "Full source"', html)
        self.assertLess(html.index('id="top"'), html.index('id="demo"'))
        self.assertLess(html.index('id="demo"'), html.index('id="method"'))
        self.assertLess(html.index('id="method"'), html.index('id="results"'))
        self.assertLess(html.index('id="results"'), html.index('id="ocr"'))
        self.assertLess(html.index('id="ocr"'), html.index('id="scope"'))
        self.assertNotIn('class="token-canvas"', html)
        self.assertNotIn("renderTokens(", html)
        self.assertNotIn('href="about.html"', html)
        self.assertNotIn('class="paper-cta"', html)
        self.assertNotIn('href="/about.html"', html)
        self.assertNotIn('href="/generate"', html)
        self.assertNotIn("Final output", html)

    def test_homepage_contains_verified_publication_details(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        about_html = (ROOT / "about.html").read_text(encoding="utf-8")

        self.assertIn(
            "Bridge continuous diffusion to a pretrained 8B backbone.", html
        )
        self.assertIn("Accepted to <strong>Findings of EMNLP 2026</strong>", html)
        self.assertIn("https://arxiv.org/abs/2606.01024", html)
        self.assertIn("assets/figure1final.png", html)
        self.assertIn("assets/nfe_efficiency_web.png", html)
        self.assertIn("assets/nfe_efficiency_web_mobile.png", html)
        self.assertIn("Copy BibTeX", html)
        self.assertIn(
            "Case study (NFE 8, 128 tokens).",
            html,
        )
        self.assertIn("length-controlled", html)
        self.assertIn("Where continuous 8B diffusion excels.", html)
        self.assertNotIn("frozen 8B architecture", html)
        self.assertNotIn("discrete and continuous quality converge", html)

        for author in (
            "Longxuan Yu",
            "Yunshu Wu",
            "Yu Fu",
            "Siheng Xiong",
            "Rob Brekelmans",
            "Hui Liu",
            "Yue Dong",
            "Greg Ver Steeg",
        ):
            self.assertIn(author, html)

        self.assertIn('content="0; url=index.html"', about_html)
        self.assertIn("window.location.replace(destination)", about_html)
        self.assertIn('href="index.html"', about_html)
        self.assertNotIn('href="/"', about_html)
        self.assertNotIn("/Users/", about_html)

    def test_paper_assets_are_published_and_served_locally(self):
        replay_server = (ROOT / "demo" / "replay_server.py").read_text(
            encoding="utf-8"
        )

        for asset in (
            "figure1final.png",
            "nfe_efficiency_web.png",
            "nfe_efficiency_web_mobile.png",
        ):
            asset_path = ROOT / "assets" / asset
            self.assertTrue(asset_path.is_file())
            self.assertGreater(asset_path.stat().st_size, 10_000)
            self.assertIn(f'"/assets/{asset}"', replay_server)

        self.assertIn(
            '"/demo/traces/ocr_impresso_case_39.json"', replay_server
        )

    def test_visible_copy_does_not_use_beta1_branding(self):
        for page in ("index.html", "about.html"):
            html = (ROOT / page).read_text(encoding="utf-8")
            visible_copy = "\n".join(
                part.split("<", 1)[0] for part in html.split(">")
            )
            self.assertNotIn("Beta1", visible_copy)
            self.assertNotIn("Beta 1", visible_copy)
            self.assertNotIn("\u2014", visible_copy)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("[DSL-LLaDA Beta1 checkpoint]", readme)

        showcase = json.loads(
            (ROOT / "demo" / "traces" / "showcase.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertNotIn("checkpoint", showcase["metadata"])

    def test_showcase_contains_matched_real_traces(self):
        showcase = json.loads(
            (ROOT / "demo" / "traces" / "showcase.json").read_text(
                encoding="utf-8"
            )
        )
        cases = showcase["cases"]

        self.assertEqual(
            [case["key"] for case in cases],
            [
                "xsum-6",
                "xsum-4",
                "xsum-16",
                "travel-anchored-1-seed1",
            ],
        )
        self.assertEqual(
            [case["task"] for case in cases],
            ["xsum", "xsum", "xsum", "travel"],
        )
        self.assertEqual(showcase["metadata"]["protocols"]["xsum-6"]["nfe"], 8)
        self.assertEqual(showcase["metadata"]["protocols"]["xsum-4"]["nfe"], 32)
        self.assertEqual(showcase["metadata"]["protocols"]["xsum-16"]["nfe"], 32)
        self.assertEqual(
            showcase["metadata"]["protocols"]["travel-anchored-1-seed1"]["nfe"],
            32,
        )
        self.assertEqual(
            showcase["metadata"]["protocols"]["travel-anchored-1-seed1"][
                "dsl_seed"
            ],
            1,
        )
        self.assertNotIn("aeslc-0", showcase["metadata"]["protocols"])

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

        travel = next(case for case in cases if case["task"] == "travel")
        summary = next(case for case in cases if case["key"] == "xsum-6")
        fasting = next(case for case in cases if case["key"] == "xsum-4")
        climate = next(case for case in cases if case["key"] == "xsum-16")
        self.assertGreater(len(summary["prompt"]), 5_000)
        self.assertIn(summary["source"], summary["prompt"])
        self.assertIn(fasting["source"], fasting["prompt"])
        self.assertIn(climate["source"], climate["prompt"])
        self.assertEqual(fasting["dsl"]["run"]["seed"], 42)
        self.assertEqual(climate["dsl"]["run"]["seed"], 42)
        self.assertNotIn("diabetes in diabetes", fasting["dsl"]["output"].lower())
        self.assertNotIn("global warming global warming", climate["dsl"]["output"].lower())
        self.assertEqual(travel["key"], "travel-anchored-1-seed1")
        self.assertEqual(travel["dsl"]["run"]["seed"], 1)
        self.assertEqual(travel["plan_evaluation"]["dsl"]["day_sections"], 3)
        self.assertEqual(
            travel["plan_evaluation"]["dsl"]["trigram_repetition_rate"],
            0.0,
        )
        self.assertNotIn("and and", travel["dsl"]["output"].lower())
        self.assertNotIn(
            "mailbox",
            json.dumps(showcase).lower(),
        )

    def test_ocr_case_uses_original_test_record_and_verified_probe(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        case = json.loads(
            (ROOT / "demo" / "traces" / "ocr_impresso_case_39.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn("Repair the errors. Preserve the document.", html)
        self.assertIn("all three official", html)
        self.assertIn("English HIPE-OCRepair domains", html)
        self.assertIn("GLCO-1850-08-13-a-p0002_par58", html)
        for word in (
            "Euglish",
            "English",
            "evice",
            "evince",
            "thander",
            "thunder",
        ):
            self.assertIn(word, html)
        self.assertIn("99.85%", html)
        self.assertIn("88.01%", html)

        provenance = case["provenance"]
        record = case["official_test_record"]
        inference = case["dsl_inference"]
        self.assertEqual(provenance["jsonl_line"], 40)
        self.assertEqual(
            provenance["dataset_commit"],
            "1bfecaf96caa01f7b80736101baad9f691904e77",
        )
        self.assertEqual(
            record["document_metadata"]["benchmark_dataset_split"], "test"
        )
        self.assertEqual(
            record["document_metadata"]["document_id"],
            "GLCO-1850-08-13-a-p0002_par58",
        )
        self.assertEqual(len(inference["changed_token_positions"]), 3)
        self.assertTrue(
            all(
                change["matches_ground_truth"]
                for change in inference["changed_token_positions"]
            )
        )
        self.assertEqual(
            inference["simple_word_edit_distance"],
            {
                "raw_ocr_to_ground_truth": 9,
                "dsl_output_to_ground_truth": 6,
            },
        )

    def test_release_excludes_large_or_runtime_only_artifacts(self):
        self.assertFalse(
            (ROOT / "demo" / "traces" / "candidate_scores.json").exists()
        )
        self.assertFalse((ROOT / "checkpoints").exists())
        self.assertFalse((ROOT / "demo" / "app.py").exists())


if __name__ == "__main__":
    unittest.main()
