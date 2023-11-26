"""
Process languages defined below, and save to ./data/

If the run should be forced (not check existing output for currentness), set 
environment variable FORCE_WIKI_RUN
"""

import datetime
import gzip
import json
import logging
import pathlib
import sys
import traceback

sys.path.append(str(pathlib.Path("./wiki_categories").absolute()))

import os
import time
from typing import Collection, Tuple

import networkx as nx
import wiki_data_dump.mirrors
from wiki_data_dump.mirrors import MirrorType

from wiki_categories.core import CategoryTree, Assets
from wiki_categories.core.category_tree import less_than_page_count_percentile
from wiki_categories.core.wiki_utils import id_for_category_str_by_lang, CategoryNotFound


def _split_lines(text: str) -> Tuple[str, ...]:
    return tuple(x.strip() for x in text.splitlines() if x.strip())


default_languages = _split_lines("""
    en
    ceb
    de
    sv
    fr
    nl
    ru
    es
    it
    arz
    ja
    zh
    vi
    uk
    ar
    pt
    fa
    ca
    sr
    ko
    no
    ce
    fi
    hu
    cs
    tt
    sh
    ro
    eu
    ms
    eo
""")

_preferred_excluded_parents = _split_lines("""
   Category:Hidden categories
   Category:Tracking categories
   Category:Container categories
   Category:Noindexed pages
   Category:Wikipedia 1.0 assessments
   Category:Wikipedia administration
   Category:Articles by importance
   Category:Articles by quality
   Category:Wikipedia categories
   Category:Stub categories
   Category:WikiProject templates
   Category:All redirect categories
""")


def save_graph_run(
        src_tree: CategoryTree,
        save_dir: pathlib.Path,
        root_id: int,
        lang: str,
        excluded_branches: Collection[str],
        page_percentile: int,
        max_depth: int,
        mutate_src: bool = True):

    if not mutate_src:
        src_tree = src_tree.copy()
        #  Shallow copy is sufficient. Node attributes may be shared.

    total_excluded = set()

    for excluded in excluded_branches:
        try:
            excluded_id = id_for_category_str_by_lang(lang, excluded, "en")
        except CategoryNotFound:
            continue

        total_excluded.update(src_tree.successors(excluded_id))
        total_excluded.add(excluded_id)

    src_tree.remove_nodes_from(total_excluded)

    reachable = nx.dfs_tree(src_tree, source=root_id, depth_limit=max_depth)
    src_tree.remove_nodes_from([x for x in src_tree if x not in reachable])

    to_remove = less_than_page_count_percentile(src_tree, page_percentile)

    for n in to_remove:
        if n == root_id:
            continue
        src_tree.remove_node_reconstruct(n)

    for x in src_tree.nodes:
        attr_dict = src_tree.nodes[x]

        output_dict = {
            "name": attr_dict["name"],
            "id": x,
            "predecessors": [
                {"name": src_tree.nodes[n]["name"], "id": n} for n in src_tree.predecessors(x)
            ],
            "successors": [
                {"name": src_tree.nodes[n]["name"], "id": n} for n in src_tree.successors(x)
            ]
        }

        with open(save_dir.joinpath(f"{x}.json"), 'w', encoding="utf-8") as f:
            json.dump(output_dict, f, ensure_ascii=False)

    with gzip.open(save_dir.joinpath("_index.txt.gz"), 'wt') as f:
        for n in src_tree.nodes:
            f.write(f"{n} {src_tree.nodes[n]["name"]}\n")


def process_language(lang: str, save_dir: pathlib.Path, force: bool = False) -> bool:
    started = time.time()
    assets = Assets(lang, wiki_dump=wiki_data_dump.WikiDump(mirror=MirrorType.WIKIMEDIA))

    page_table_updated = assets.page_table_job.updated
    category_links_updated = assets.category_links_job.updated
    category_table_updated = assets.category_table_job.updated

    page_percentile = 70
    max_depth = 100

    if not force and save_dir.joinpath("_meta.json").exists():
        try:
            with open(save_dir.joinpath("_meta.json"), 'r', encoding="utf-8") as f:
                meta_json = json.load(f)

            assert meta_json["page_table_updated"] == page_table_updated
            assert meta_json["category_links_updated"] == category_links_updated
            assert meta_json["category_table_updated"] == category_table_updated
            assert meta_json["page_percentile"] == page_percentile
            assert meta_json["max_depth"] == max_depth

            return False
            #  Skip run
        except KeyError:
            pass
        except AssertionError:
            pass
        except json.JSONDecodeError:
            pass

    save_dir.mkdir(exist_ok=True)

    for file_name in os.listdir(save_dir):
        file_name = str(file_name)

        if file_name.endswith(".json") or file_name.endswith(".txt.gz"):
            os.unlink(save_dir.joinpath(file_name))

    save_graph_run(
        CategoryTree(assets),
        save_dir,
        root_id=id_for_category_str_by_lang(lang, "Category:Contents", "en"),
        lang=lang,
        excluded_branches=_preferred_excluded_parents,
        page_percentile=page_percentile,
        max_depth=max_depth,
        mutate_src=True
    )

    with open(save_dir.joinpath("_meta.json"), 'w', encoding="utf-8") as f:
        duration = int(time.time() - started)

        json.dump({
            "page_table_updated": page_table_updated,
            "category_links_updated": category_links_updated,
            "category_table_updated": category_table_updated,
            "page_percentile": page_percentile,
            "max_depth": max_depth,
            "run_duration_seconds": duration,
            "finished": datetime.datetime.now().isoformat()
        }, f)

    return True


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    _force = True if "FORCE_WIKI_RUN" in os.environ else False

    started = datetime.datetime.now()

    root = pathlib.Path("./data")

    root.mkdir(exist_ok=True)

    languages_processed = []
    incomplete_languages = []

    for index, language in enumerate(default_languages):
        logging.info(f"Starting {language}wiki at {datetime.datetime.now()}. {index + 1} of {len(default_languages)}")

        try:
            finished = process_language(language, root.joinpath(language), force=_force)

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
