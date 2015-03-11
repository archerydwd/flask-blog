# Flask-blog

Please note this is not a tutorial, I have wrote it in that style so you can follow along. If you get into trouble (like I did) try the mailing list or just google it. You will find that you will actually learn more from researching it and getting into tight spots. ;) 

I built this app with the Flask micro-framework to be used as part of a series of applications that I will be 
performing tests on. This is a Flask version of the Ruby on Rails blog application: https://github.com/archerydwd/rails-blog & the Chicago Boss version is here: https://github.com/archerydwd/cb-blog

I am going to be performing tests on this app using some load testing tools such as Gatling & Tsung. 

Once I have tested this application and the other verisons of it, I will publish the results, which can then be used as a benchmark for others when trying to choose a framework.

You can build this app using a framework of your choosing and then follow the testing mechanisms that I will describe and then compare the results against my benchmark to get an indication of performance levels of your chosen framework.

==
###Installing Flask
==

At time of writing this the Python version was: 2.7.9 and the Flask version was: 0.10.1

**Install Python**

On OSX follow the link: https://www.python.org/ftp/python/2.7.9/python-2.7.9-macosx10.6.pkg
Open this and follow the instructions.

On Linux

wget http://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
tar -xzf Python-2.7.9.tgz  
cd Python-2.7.9

./configure  
make  
sudo make install


**Install Flask**

On OSX:

```
pip install Flask
```

