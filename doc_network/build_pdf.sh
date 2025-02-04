docker run --rm -v "$(pwd):/data" -u "$(id -u)" pandocscholar/alpine
cp out.pdf mapping_at_scale.pdf
cp out.latex mapping_at_scale.tex
