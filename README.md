# wiki_categories_datastore

> [!WARNING]  
> This is no longer deployed automatically. If you need automatic 
> deployments, fork this repository and place `update.yml.old` in 
> your workflows directory, fixing its file extension.
> 
> Also, I've made a more compact (and accessible, it uploads to GH Pages 
> only instead of the actual repo) version called [wiki-categories](
    https://github.com/jon-edward/wiki-categories).

This repository contains automatic deployments of the Wikipedia category tree, trimmed by the algorithm defined in 
[main](https://github.com/jon-edward/wiki_categories_datastore/blob/main/main.py).

**The data stored here does not contain faithful reproductions of the Wikipedia category trees. To make a 
trimmed category tree, many categories are excluded and there are many edges added that do not exist in their respective 
true category graphs.**

To construct the full (untrimmed) category tree, see [CategoryTree](https://github.com/jon-edward/wiki_categories/blob/main/wiki_categories/core/category_tree.py) 
and [Assets](https://github.com/jon-edward/wiki_categories/blob/main/wiki_categories/core/assets/__init__.py),

Assets are sourced from the [Wikimedia data dumps](https://dumps.wikimedia.org/).

## Format

For each language contained in `./data/` there is a `_meta.json` file that contains information about the last successful run, 
`_index.bytes` that is a concatenated, zero-padded (big-endian) list of unsigned 4-byte integers for the available 
category IDs, and category files in the file name format `[0-9]+\.json` that describe the category's name, successors, and predecessors.

## Languages

Deployments are available for the following Wikipedia languages:
 - [ar](https://ar.wikipedia.org)
 - [arz](https://arz.wikipedia.org)
 - [ca](https://ca.wikipedia.org)
 - [ce](https://ce.wikipedia.org)
 - [ceb](https://ceb.wikipedia.org)
 - [cs](https://cs.wikipedia.org)
 - [de](https://de.wikipedia.org)
 - [en](https://en.wikipedia.org)
 - [eo](https://eo.wikipedia.org)
 - [es](https://es.wikipedia.org)
 - [eu](https://eu.wikipedia.org)
 - [fa](https://fa.wikipedia.org)
 - [fi](https://fi.wikipedia.org)
 - [fr](https://fr.wikipedia.org)
 - [hu](https://hu.wikipedia.org)
 - [it](https://it.wikipedia.org)
 - [ja](https://ja.wikipedia.org)
 - [ko](https://ko.wikipedia.org)
 - [ms](https://ms.wikipedia.org)
 - [nl](https://nl.wikipedia.org)
 - [no](https://no.wikipedia.org)
 - [pt](https://pt.wikipedia.org)
 - [ro](https://ro.wikipedia.org)
 - [ru](https://ru.wikipedia.org)
 - [sh](https://sh.wikipedia.org)
 - [sr](https://sr.wikipedia.org)
 - [sv](https://sv.wikipedia.org)
 - [tt](https://tt.wikipedia.org)
 - [uk](https://uk.wikipedia.org)
 - [vi](https://vi.wikipedia.org)
 - [zh](https://zh.wikipedia.org)

## Disclaimer

The author of this software is not affiliated, associated, authorized, endorsed by, or in any way 
officially connected with The Wikimedia Foundation or any of its affiliates and is independently 
owned and created.
