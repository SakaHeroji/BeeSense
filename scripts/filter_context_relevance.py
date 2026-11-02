"""Filter a verified existing corpus into a new auditable relevance dataset."""

import argparse
import json
from pathlib import Path

from MachineLearning.context_relevance import ContextRelevanceFilter
from MachineLearning.relevance_semantic import LocalSemanticBackend
from MachineLearning.social_nlp import SocialNLPClusterer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("Output exists; choose a new experiment directory")
    data = SocialNLPClusterer.load_run(args.source_run)

    def progress(event):
        print(json.dumps(event, ensure_ascii=False), flush=True)

    filterer = ContextRelevanceFilter(args.config, progress=progress)
    try:
        filterer.predictor = LocalSemanticBackend(filterer.config, source_data=data)
        output = filterer.filter_snapshot(data, args.output_dir)
        progress({"event": "relevance_complete", "output_dir": str(output)})
    finally:
        filterer.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
