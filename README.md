# S2TT
Python program using Watson's "Speech to Text" service to transcribe an audio source (as a PoC, only supports English and French at the moment) and then "Language Translator v3" to translate the transcript in the requested language. To do so, this software makes use of API requests.
The GUI is made with tkinter library.  
Watson may be a bit slow to answer depending on the size of your audio file, it is recommended to test with short samples.

## Repository structure
The first version is the standalone file "S2tt.py" \
The object-oriented version is in the folder "ObjectOrientedVersion"
