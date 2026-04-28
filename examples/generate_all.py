"""Run all example scripts and save outputs to example_output/."""

import os
import glob
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = os.path.join(ROOT, "example_output")
os.makedirs(OUT, exist_ok=True)

examples_dir = os.path.join(ROOT, "examples")
scripts = sorted(glob.glob(os.path.join(examples_dir, "[0-9]*.py")))

print(f"Running {len(scripts)} examples...\n")

for script in scripts:
    name = os.path.basename(script)
    print(f"  {name}...", end=" ", flush=True)
    try:
        with open(script) as f:
            code = f.read()
        exec(compile(code, script, "exec"), {"__name__": "__main__"})
        print("OK")
    except Exception as e:
        print(f"FAILED: {e}")

n_pngs = len(glob.glob(os.path.join(OUT, "*.png")))
print(f"\nDone! {n_pngs} images in {OUT}/")
