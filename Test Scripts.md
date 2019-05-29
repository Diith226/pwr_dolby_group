# **Test script 1:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Load file** button and highlight **Cancel** button (without clicking it), or choose a file  
**Expected result:** Opened file explorer waits until user choose file or decide to cancel   
**Result:** Application crash  
**Solved:** No  
**Notes:** Probably threads problems  

```python
CoCreateInstance failed (Operacja uko˝czona pomyťlnie.)
QObject: Cannot create children for a parent that is in a different thread.
(Parent is QApplication(0x2565bf2d930), parent's thread is QThread(0x25657b40870), current thread is LoadThread(0x2565bf39e40)
CoCreateInstance failed (Operacja uko˝czona pomyťlnie.)
```  

# **Test script 2:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Start dreaming** button (without loading file)   
**Expected result:** New window informs user to load file first / nothing happens   
**Result:** Application crash  
**Solved:** No  
**Notes:** Button can be disabled until user load file 

``` python
Traceback (most recent call last):  
  File "GUI_X1_3.py", line 37, in run  
    dream_result = deep_dream.backend(self.GUI.filepC:\Users\pawel\Anaconda3\envs\dolby\lib\site-packages\matplotlib\figure.py:98: MatplotlibDeprecationWarning:  
Adding an axes using the same arguments as a previous axes currently reuses the earlier instance.  In a future version, a new instance    will always be created and returned.  Meanwhile, this warning can be suppressed, and the future behavior ensured, by passing a unique   label to each axes instance.  
  "Adding an axes using the same arguments as a previous axes "  
ath, self.GUI.dreamStream)  
AttributeError: 'Ui_DeepDreamSound' object has no attribute 'filepath'  
```  

# **Test script 3:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Save dream** button and highlight cancel button (without loading file and start dreaming)  
**Expected result:** New window informs user to load file and start dreaming first / nothing happens   
**Result:** Application crash  
**Solved:** No  
**Notes:** Button can be disabled until user load file 

```python
CoCreateInstance failed (Operacja uko˝czona pomyťlnie.)  
QFileSystemWatcher: Removable drive notification will not work if there is no QCoreApplication instance.  
QObject::startTimer: Timers can only be used with threads started with QThread  
QObject: Cannot create children for a parent that is in a different thread.  
(Parent is QApplication(0x16c9bf817d0), parent's thread is QThread(0x16c97b798c0), current thread is QThread(0x16c9c6fddf0)  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QObject::startTimer: Timers can only be used with threads started with QThread  
QObject::startTimer: Timers can only be used with threads started with QThread  
QObject::startTimer: Timers can only be used with threads started with QThread  
QObject::startTimer: Timers can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
CoCreateInstance failed (Operacja uko˝czona pomyťlnie.)  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread  
QObject::startTimer: Timers can only be used with threads started with QThread  
QBasicTimer::stop: Failed. Possibly trying to stop from a different thread  
QBasicTimer::stop: Failed. Possibly trying to stop from a different thread  
QBasicTimer::start: Timers cannot be started from another thread  
```  


# **Test script 4:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Save dream** button, then close file explorer and click **Load file** button. Close opened explorer  
**Expected result:** Both opened explorers should have same style and can be closed without problems.  
**Result:** After click **Load file** button, file explorer will have another style. Closing it make whole application crash   
**Solved:** No  
**Notes:** First style of file explorer looks like linux one, second have windows type  

```python
CoCreateInstance failed (Operacja uko˝czona pomyťlnie.)
QFileSystemWatcher: Removable drive notification will not work if there is no QCoreApplication instance.
QObject::startTimer: Timers can only be used with threads started with QThread
QObject: Cannot create children for a parent that is in a different thread.
(Parent is QApplication(0x1b7e0af9170), parent's thread is QThread(0x1b7dc6da4e0), current thread is QThread(0x1b7e126c760)
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QObject::startTimer: Timers can only be used with threads started with QThread
QObject::startTimer: Timers can only be used with threads started with QThread
QObject::startTimer: Timers can only be used with threads started with QThread
QObject::startTimer: Timers can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
CoCreateInstance failed (Operacja uko˝czona pomyťlnie.)
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
QObject::startTimer: Timers can only be used with threads started with QThread
QBasicTimer::stop: Failed. Possibly trying to stop from a different thread
QBasicTimer::stop: Failed. Possibly trying to stop from a different thread
QBasicTimer::start: Timers cannot be started from another thread
Unhandled exception in thread started by <bound method Ui_DeepDreamSound.saveFile of <__main__.Ui_DeepDreamSound object at 0x000001B7CCBBF940>>
Traceback (most recent call last):
  File "GUI_X1_3.py", line 378, in saveFile
    librosa.output.write_wav(filename, self.dreamt_signal, self.dreamt_sr)
AttributeError: 'Ui_DeepDreamSound' object has no attribute 'dreamt_signal'
Traceback (most recent call last):
  File "GUI_X1_3.py", line 97, in run
    self.GUI.x, self.GUI.sr = librosa.load(filename)
  File "C:\Users\pawel\Anaconda3\envs\dolby\lib\site-packages\librosa\core\audio.py", line 119, in load
    with audioread.audio_open(os.path.realpath(path)) as input_file:
  File "C:\Users\pawel\Anaconda3\envs\dolby\lib\site-packages\audioread\__init__.py", line 80, in audio_open
    return rawread.RawAudioFile(path)
  File "C:\Users\pawel\Anaconda3\envs\dolby\lib\site-packages\audioread\rawread.py", line 61, in __init__
    self._fh = open(filename, 'rb')
PermissionError: [Errno 13] Permission denied: 'C:\\Users\\pawel\\Documents\\GitHub\\pwr_dolby_group'
```  
# **Test script 5:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Save dream** button, then close file explorer and click **Load file** button. Choose file and click **Otwórz** button  
**Expected result:** Program will crash when user will try to load a file (as in **Test script 1**)  
**Result:** After click **Load file** button, file explorer will have another style. With second style, file can be loaded, and program   works without crashes  
**Solved:** No  
**Notes:** First style of file explorer looks like linux one, second have windows type. Second type of explorer works better in this     case  
