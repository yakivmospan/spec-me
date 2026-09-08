#!/usr/bin/env python3
"""Put one original run beside one intest run and write the comparison down.

The behaviour suite's own `--compare` prints dimensions side by side. This adds the half that needs
no agent — what each shape costs in always-on words — and writes both into one file that can be read
months later without rerunning anything.

    python3 compare.py --original <a.json> --intest <b.json> --manifest /tmp/rules-vs-skills/manifest.json
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


def cases_of(record):
    out = {}
    for run in record.get("runs", []):
        for case in run.get("cases", []):
            out[case["id"]] = case
    return out


def verdict(a, b):
    if abs(a - b) < 0.005:
        return "same"
    return "intest better" if b > a else "**original better**"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--original", required=True)
    ap.add_argument("--intest", required=True)
    ap.add_argument("--manifest")
    ap.add_argument("--out", help="where to write; defaults into results/")
    args = ap.parse_args()

    a = json.loads(Path(args.original).read_text())
    b = json.loads(Path(args.intest).read_text())
    ca, cb = cases_of(a), cases_of(b)

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [f"# original vs intest — {stamp}", "",
             f"- builder `{a.get('builder','?')}`, agent `{a.get('agent','?')}`, "
             f"{a.get('repeats', 1)} take(s) per case",
             "- **original**: on-demand rules reached through `LOADER.md` rows",
             "- **intest**: every on-demand rule converted to a skill, on-demand table empty", ""]

    if args.manifest:
        m = json.loads(Path(args.manifest).read_text())
        x, y = m["cost"]["original"], m["cost"]["intest"]
        lines += [f"Descriptions in the intest tree were **{m['descriptions']}**.", "",
                  "## What each shape costs before any request", "",
                  "| | original | intest | change |", "|---|---:|---:|---:|"]
        for key, label in (("always_on_rules", "always-on rules"),
                           ("skill_descriptions", "skill descriptions"),
                           ("loaders", "loaders"), ("total", "**total**")):
            lines.append(f"| {label} | {x[key]} | {y[key]} | {y[key] - x[key]:+} |")
        lines.append(f"| skills listed | {x['skills']} | {y['skills']} | {y['skills'] - x['skills']:+} |")
        lines.append("")

    lines += ["## Did the guidance get reached", "",
              "| case | original | intest | |", "|---|---:|---:|---|"]
    for cid in sorted(set(ca) | set(cb)):
        sa = ca.get(cid, {}).get("score")
        sb = cb.get(cid, {}).get("score")
        fa = "—" if sa is None else f"{sa:.0%}"
        fb = "—" if sb is None else f"{sb:.0%}"
        mark = "" if sa is None or sb is None else verdict(sa, sb)
        lines.append(f"| `{cid}` | {fa} | {fb} | {mark} |")

    both = [(ca[c]["score"], cb[c]["score"]) for c in set(ca) & set(cb)]
    if both:
        ma = sum(x for x, _ in both) / len(both)
        mb = sum(y for _, y in both) / len(both)
        lines += ["", f"**Overall: original {ma:.0%}, intest {mb:.0%} — {verdict(ma, mb)}.**", ""]

    misses = []
    for cid in sorted(set(ca) & set(cb)):
        for side, rec in (("original", ca[cid]), ("intest", cb[cid])):
            for chk in rec.get("checks", []):
                if not chk.get("pass"):
                    misses.append(f"- `{cid}` ({side}): missed {chk['label']}")
    if misses:
        lines += ["## Every check that missed", ""] + misses + [""]

    out = Path(args.out) if args.out else HERE / "results" / f"{stamp.replace(':','').replace('-','')}-comparison.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nwritten to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
