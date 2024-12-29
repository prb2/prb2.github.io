#!/bin/sh

echo "Building blog index..."

# echo "<link rel=\"stylesheet\" href=\"./style.css\">\n\n" > ./src/blog.md
echo "---\ntitle: Blog\n---" > ./src/blog.md
echo "## Blog\n" >> ./src/blog.md
for f in $(ls -r src/posts/*.md)
do
    echo "\t$f";
    fname=$(echo "$f" | sed 's|^src|build|; s|\.md$|.html|')
    echo "[$(head -n 1 $f | sed 's/# //')]($fname)\n" >> ./src/blog.md
done

echo "Generating html..."
for f in $(ls -r src/*.md src/posts/*.md)
do
    fname=$(echo "$f" | sed 's|^src|build|; s|\.md$|.html|')
    echo "\tgenerating $fname"
    echo "<link rel=\"stylesheet\" href=\"../style.css\">" > $fname
    cat src/sidebar.template >> $fname
    # need to use "-f markdown-smart" so that quote marks and other ligatures look correct
    pandoc -f markdown-smart -t html $f | sed 's/↩/\&\#x21A9;/g' >> $fname
done

# TODO: use a custom html template
# https://www.arthurkoziel.com/convert-md-to-html-pandoc/

echo "Done"
