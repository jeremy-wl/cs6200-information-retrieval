### A one or two sentence answer each to the questions: What was the most difficult part of this assignment? What was the easiest part?

- the most difficult part
  - the indexing step where we need to create 3 files
  - understanding the purpose of those 3 files
- the easiest part
  - the query step, since we have all data structures we need, implementing the querying methods
    does not take much effort

### Details about the format of the 3 index files (described in Part 2) you created.

- TermIDFile: a simple csv file with [term_id, term, freq] as fields
- DocumentIDFile: a simple csv file with [doc_id, doc_name, num_terms] as fields
- InvertedIndex: a json file directly mapped from a dict, where key is the doc_id,
                 and value is a list of postings

### A run of the query Q and the results you got (see Part 3).

Querying term 'asterisk' will give us results below:
```
Searching for term asterisk in all docs...

011_Full-text_search.txt
239_List_of_Fields_Medal_winners_by_university_affiliation.txt
613_Unix.txt
710_Internet_forum.txt
786_Skype.txt
843_Plain_text.txt
846_Asterisk.txt
890_Proximity_search_(text).txt
```
