# **Test script 1:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click “Load file” button and highlight cancel button (without clicking it)  
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
**Action:** Open application, click "Start dreaming" button (without loading file) 
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
