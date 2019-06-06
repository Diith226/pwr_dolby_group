# **Bug 1:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Load file** button and highlight **Cancel** button (without clicking it), or choose a file  
**Expected result:** Opened file explorer waits until user choose file or decide to cancel   

# **Bug 2:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Start dreaming** button (without loading file)   
**Expected result:** New window informs user to load file first / nothing happens   

# **Bug 3:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Save dream** button and highlight cancel button (without loading file and start dreaming)  
**Expected result:** New window informs user to load file and start dreaming first / nothing happens   


# **Bug 4:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Save dream** button, then close file explorer and click **Load file** button. Close opened explorer  
**Expected result:** Both opened explorers should have same style and can be closed without problems.  
# **Bug 5:**  
**Author:** Paweł Oberc  
**Date:** 29.05.2019  
**Conda version:** conda 4.6.14  
**Python version:** Python 3.7.2  
**Environment:** https://github.com/226776/pwr_dolby_group/blob/master/env.yml  
**Action:** Open application, click **Save dream** button, then close file explorer and click **Load file** button. Choose file and click **Otwórz** button  
**Expected result:** Program will crash when user will try to load a file (as in **Test script 1**)  
