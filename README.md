# DeepDreamSound
Repository of the Dolby project
## Overview

The project is inspired by Google DeepDream technique, which enchances the features found by neural network to create impressionist/abstractionist art inspired by image fed to the network. As inspired by the Google paper on the subject of DeepDream, our project will have it's own network trained to recognize music genres (or even bands), which is able to extract features of given music and enchance them creating something new. The recognition and enchancement will happen on data in form of raw signal samples or on spectrograms (or melgrams, as they're more natural for music).

## Features

The application will have GUI with an option to load music file (.wav format - or similar if we are able to program the feature). The loaded file could be then processed and as a result the user shall recieve network's impression of the file. The GUI will also consist of:
* Spectrograms for input and output file
* Players for input and output file
* Load and Save options (at least .wav files)
* Additional modifiable parameters of the DeepDream generation

## How To
* Git-LFS is needed to clone the repository
* Install the anaconda from the anaconda page (https://www.anaconda.com/distribution/)
* Install the environment from the .yml file

```
conda env create -f environment.yml
```

* Run the app

```
python GUI_X1_3.py
```

* Load the music file by clicking on the ... button -> The file will be loaded, and the spectrogram created
* Click start dreaming button to start the dream process


## Our Team
* Kacper Kania
* Krystian Kasprów
* Cyprian Mataczyński
* Paweł Oberc
