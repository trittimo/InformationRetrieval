This requires Python 3 in order to run.

I use the program as follows:

py info.py <dataset folder>
OR
py info.py <dataset folder> [search phrases] ...

The first will let you enter as many phrases as you want, reading them as you go and outputting them on the command line

The second version will use the search phrases you provide and analyze them all at once, spitting them back on the command line (which can then be redirected to a file). For example, if I wanted to look for "lincoln assassinated" and "taft" as my search phrases, I could do the following:

py info.py data/presidents "lincoln assassinated" "taft" > some_output_file.txt