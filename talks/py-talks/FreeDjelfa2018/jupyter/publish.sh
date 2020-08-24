#!/bin/bash

echo "Remove slides_djelfa2018.slides.html file "
rm -f slides_djelfa2018.slides.html

jupyter nbconvert slides_djelfa2018.ipynb --to slides --post serve --ServePostProcessor.reveal_cdn="http://cdn.jsdelivr.net/reveal.js/2.5.0"


