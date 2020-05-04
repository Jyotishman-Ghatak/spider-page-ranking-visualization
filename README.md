# Spider-Page-Ranking-Visualization
This set of programs emulate some of the functions of a search engine. The data is stored in a [SQLITE 3](https://www.sqlite.org) database name [spider.sqlite](../blob/master/spider.sqlite)

You need to download [DB browser](https://sqlitebrowser.org/dl/) to view and modify data.

## Libraries/Modules Used:
* **Beautiful Soup**
* **urllib**
* **ssl**
* **D3.v2.js**


## USAGE
#### Execution of programs are done in following manner
* **spider.py:** This program crawls a web site and pulls a series of pages into the database, recording the links between pages. User is asked to enter a website followed by a '/' at the end and number of pages to spider. The retrieved urls are stored with a initial page rank as 1.0. 

* **sprank.py:** Ranking of page is done using the Page Rank Algrotihm which is given by the expression
