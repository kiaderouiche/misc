#!/bin/bash

jupyter nbconvert slides.ipynb --to slides --post serve 
--ServePostProcessor.reveal_cdn="http://cdn.jsdelivr.net/reveal.js/2.5.0"


