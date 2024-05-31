#!/bin/sh

echo "Building blog index..."

echo "<link rel=\"stylesheet\" href=\"./style.css\">\n\n" > ./blog.md
echo "# Blog Posts\n" >> ./blog.md
for f in $(ls -r posts/*.md)
do
    echo "\t$f";
    fname=$(echo "$f" | cut -f 1 -d '.')".html"
    echo "[$(head -n 1 $f | sed 's/# //')]($fname)\n\n" >> ./blog.md
done

echo "Generating html..."
for f in $(ls -r *.md posts/*.md)
do
    fname=$(echo "$f" | cut -f 1 -d '.')".html"
    echo "\tgenerating $fname"
    echo "<link rel=\"stylesheet\" href=\"../style.css\">" > ../$fname
    cat sidebar.template >> ../$fname
    pandoc -t html $f | sed 's/↩/\&\#x21A9;/g' >> ../$fname
done


echo "Done"
