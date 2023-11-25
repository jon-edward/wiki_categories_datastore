import datetime
import json
import logging
import pathlib
import sys
import traceback

sys.path.append(str(pathlib.Path("./wiki_categories").absolute()))

from wiki_categories.scripts.save_graph_run import process_language, default_languages


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    started = datetime.datetime.now()

    root = pathlib.Path("./data")

    root.mkdir(exist_ok=True)

    languages_processed = []
    incomplete_languages = []

    for index, language in enumerate(default_languages):
        logging.info(f"Starting {language}wiki at {datetime.datetime.now()}. {index + 1} of {len(default_languages)}")

        try:
            finished = process_language(language, root.joinpath(language))

            if finished:
                languages_processed.append(language)
        except:
            incomplete_languages.append(language)
            logging.error(traceback.format_exc())

        logging.info(f"Finished {language}wiki at {datetime.datetime.now()}.")

    with open(root.joinpath("_meta.json"), 'w', encoding="utf-8") as f:
        json.dump({
            "started": started.isoformat(),
            "finished": datetime.datetime.now().isoformat(),
            "languages_processed": languages_processed,
            "incomplete_languages": incomplete_languages
        }, f)
