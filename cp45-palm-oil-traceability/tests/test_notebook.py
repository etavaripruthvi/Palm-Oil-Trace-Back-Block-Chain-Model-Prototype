"""Execute every code cell of the notebook (headless, synthetic panel) to prove the pipeline runs end to end.

Set CP45_SKIP_SLOW=1 to skip. Optional libraries (xgboost, shap) are not required: the notebook falls back gracefully.
"""
import contextlib
import io
import json
import os
import unittest

import matplotlib
matplotlib.use("Agg")

import _paths
from _paths import ROOT


@unittest.skipIf(os.environ.get("CP45_SKIP_SLOW") == "1", "slow test skipped")
class NotebookRuns(unittest.TestCase):
    def test_all_code_cells_execute(self):
        nb = json.loads((ROOT / "notebooks" / "CP45_Palm_Oil_Traceability_Notebook.ipynb").read_text(encoding="utf-8"))
        code = [("".join(c["source"])) for c in nb["cells"] if c["cell_type"] == "code"]
        self.assertGreaterEqual(len(code), 8)
        ns = {"display": lambda x: print(x.to_string() if hasattr(x, "to_string") else x), "__name__": "__main__"}
        cwd = os.getcwd()
        os.chdir(ROOT / "notebooks")
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                for i, src in enumerate(code):
                    try:
                        exec(compile(src, f"<cell {i}>", "exec"), ns)
                    except Exception as e:                            # report which cell failed
                        self.fail(f"code cell {i} failed: {type(e).__name__}: {e}")
        finally:
            os.chdir(cwd)
        out = buf.getvalue()
        self.assertIn("SYNTHETIC - code test, NOT EVIDENCE", out)    # no real panel shipped -> every classifier number is tagged
        self.assertIn("Model module loaded. Seed: 42", out)


if __name__ == "__main__":
    unittest.main()
