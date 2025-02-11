docker run --rm -v "$(pwd):/data" -u "$(id -u)" pandocscholar/alpine
cp out.pdf teds.pdf
cp out.latex teds.tex