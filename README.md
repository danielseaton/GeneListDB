# GeneListDB
Basic scripting to create mySQL database storing Arabidopsis gene lists from publications (e.g. lists of differentially expressed genes in mutants or treatments, lists of promoters identified as bound by ChIP-seq).

## Adding lists to an existing database

Add gene lists to an existing database using 'load_gene_lists.py', by specifying a directory to search for '.genelist' files, and a database file to which they should be added.

The '.genelist' files are tab delimited text files with a header followed by a list of locus identifiers, taking the form:

```
list_name<\t>description<\t>PMID
locus_id_0
locus_id_1
locus_id_2
...
```

list_name should be a unique identifier. locus IDs should be of the standard form (e.g. AT1G09570 for PHYA). PMID is the pubmed ID of the associated paper (if relevant).


## Creating a new database

Choose the name for the database by editing the 'initialise_table_schema.py' script (default is "GeneListDB.db"), then running it. Gene lists can then be added as described above
