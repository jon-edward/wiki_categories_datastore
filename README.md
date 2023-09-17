# wiki_categories_datastore

This repository contains automatic deployments of the Wikipedia category tree in JSON format.

Each language includes metadata for when each source was last updated on the data dump mirror; the full 
category tree with category names, edges, and page count (compressed in gzip format); and a plain-text trimmed category tree. 

The trimmed category tree contains categories with page counts higher than the 65th percentile of all 
categories in the language (excluding main topic classifications, which are not trimmed regardless), 
then trimmed to a distance of at most 99 steps from a main topic classification.

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
 - [pl](https://pl.wikipedia.org)
 - [pt](https://pt.wikipedia.org)
 - [ro](https://ro.wikipedia.org)
 - [ru](https://ru.wikipedia.org)
 - [sh](https://sh.wikipedia.org)
 - [sr](https://sr.wikipedia.org)
 - [sv](https://sv.wikipedia.org)
 - [tr](https://tr.wikipedia.org)
 - [tt](https://tt.wikipedia.org)
 - [uk](https://uk.wikipedia.org)
 - [vi](https://vi.wikipedia.org)
 - [zh](https://zh.wikipedia.org)

## Disclaimer

The author of this software is not affiliated, associated, authorized, endorsed by, or in any way 
officially connected with The Wikimedia Foundation or any of its affiliates and is independently 
owned and created.
