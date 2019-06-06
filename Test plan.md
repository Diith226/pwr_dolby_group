# Test Plan for DeepDreamSound Application 

Author: Krystian Kasprów


## Manual Test 1

### Procedure:
Open application ---> click **Tool Button** ---> choose wave file

### Expected result: 
Wave file succesfully loaded, spectrogram ploted correctly

## Manual Test 2

### Procedure:
Open application ---> click **Tool Button** --->choose mp3 file 

### Expected result: 
Mp3 file succesfully loaded, spectrogram ploted correctly

## Manual Test 3

### Procedure:
Open application ---> click **Tool Button** ---> choose file ---> click **Start Dreaming**

### Expected result: 
Application starts to processing input signal and the progress bar apears.

## Manual Test 4

### Procedure:
Open application ---> wait (no longer than 1h)

### Expected result: 
Application runs, and waits for user action.


## Manual Test 5

### Procedure:
Open application ---> click **Load file** button ---> highlight **Cancel** button (without clicking it) or choose a file  

### Expected result: 
Application opens file browser window, than waits for user to choose file and confirm

## Manual Test 6

### Procedure:
Open application ---> click **Tool Button** ---> choose file ---> click **Start Dreaming**---> wait until processing finishes ---> click **Save Dream** ---> choose the dream file location and name ---> confirm 

### Expected result: 
Application succesfully generates output file. Output file is functional. 

## Manual Test 7

### Procedure:
Open application ---> click **Start dreaming** button (without loading file)  

### Expected result: 
New window informs user to load file first / nothing happens

## Manual Test 8

### Procedure:
Open application ---> click **Save dream** button ---> highlight cancel button (without loading file and start dreaming)  

### Expected result: 
New window informs user to load file and start dreaming first / nothing happens   

## Manual Test 9

### Procedure:
Open application ---> click **Save dream** button ---> close file explorer and click **Load file** button. Close opened explorer 

### Expected result: 
Both opened explorers should have same style and can be closed without problems. 

## Manual Test 10

### Procedure:
Open application ---> massive click every button 

### Expected result: 
Application doesn't crashes, and reacts propertly for each button.
