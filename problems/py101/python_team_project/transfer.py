
# coding: utf-8

# In[1]:


my_string = "add Tathagata Dasgupta 1"


# In[11]:


name_lines = my_string.split('add ')[1]


# In[12]:


import re


# In[13]:


num_lines = name_lines.rsplit()[-1]


# In[18]:


name = name_lines.rsplit()[:-1]


# In[21]:


name_part = ' '.join(name)


# In[ ]:




