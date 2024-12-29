#!/bin/sh

echo "Building blog index..."

# echo "<link rel=\"stylesheet\" href=\"./style.css\">\n\n" > ./src/blog.md
echo "---\ntitle: Blog\n---" > ./src/blog.md
for f in $(ls -r src/posts/*.md)
do
    echo "\t$f";
    fname=$(echo "$f" | sed 's|^src||; s|\.md$|.html|')
    title=$(grep '^title:' $f | cut -d ' ' -f 2-)
    date=$(grep '^date:' $f | cut -d ' ' -f 2-)
    echo "$date | [$title]($fname)\n" >> ./src/blog.md
done

echo "Removing old html files..."
find ./build -name "*.html" -type f -delete

echo "Generating html..."
for f in $(ls -r src/*.md src/posts/*.md)
do
    fname=$(echo "$f" | sed 's|^src|build|; s|\.md$|.html|')
    echo "\tgenerating $fname"
    cat src/sidebar.template > $fname
    # need to use "-f markdown-smart" so that quote marks and other ligatures look correct
    pandoc -s -c /style.css -f markdown-smart -t html $f | sed 's/↩/\&\#x21A9;/g' >> $fname
done

# TODO: use a custom html template
# https://www.arthurkoziel.com/convert-md-to-html-pandoc/

echo "Done"
