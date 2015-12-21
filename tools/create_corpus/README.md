Elpod create corpus from wikipedia and twitter.

Wikipedia
-------------
create wikipedia corpus manually.
download articles.
http://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
$ wp2txt --input-file jawiki-latest-pages-articles.xml.bz2 -o ../../corpus/wikipedia --no-list --no-heading --no-marker -f 100

Twitter
-------------
