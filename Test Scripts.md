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
