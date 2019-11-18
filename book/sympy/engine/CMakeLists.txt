PROJECT ( master_project  NONE ) 
cmake_minimum_required ( VERSION  2.8 ) 
SET ( LATEX_OUTPUT_PATH  build ) 
INCLUDE ( UseLATEX.cmake )

file ( GLOB_RECURSE  contents_files  RELATIVE  $ { CMAKE_SOURCE_DIR }  contents / *. tex )

ADD_LATEX_DOCUMENT ( 
    main.tex 
    INPUTS $ { contents_files } 
    IMAGE_DIRS  Pictures 
    BIBFILES  bibliography.bib 
    USE_INDEX 
    USE_GLOSSARY 
    FILTER_OUTPUT 
    )
