# ToolsetUnbound23
These are the source files for the website under development which aims to provide users with the ability to compress, store, and access files present in cloud
The Report files are present in the Reports directory
# Installation Instructions  
## Installing Python Dependencies
Python dependencies can be installed by using the pip command to install from requirements.txt. Ideally using a virtual environment while doing so  
```pip install -r requirements.txt```

## Installing and creating the tables for Mysql
The MySQL server must be installed on your computer by following this [website](https://www.javatpoint.com/how-to-install-mysql).  
Create the MySQL table by using the following command in the MYSQL command line.  
  ```source path-to-cloned-repo\Databasees\UserTableCreate.sql```

# Instructions for Executing Files
The following instruction gives you a basic overview of the algorithms and software used to create the website and the means to run them.
## Instructions for Running Website
The server has been implemented by Flask, a lightweight framework in Python along with Werkzeug and other libraries.
The server can be started by going to the Website directory and using the following command  
  ```python app.py```
## Compression Algorithms

### Text Compression Algorithm
This algorithm has been implemented by the Huffman encoding which you can read more about [here](https://brilliant.org/wiki/huffman-encoding/#:~:text=Huffman%20code%20is%20a%20way,more%20rarely%20can%20be%20longer.).  
To run the text compression algorithm please run the following command in the CompressionAlg directory.  
  ```python textV1.py```

### Audio Compression Algorithm
The audio compression works by a lossy algorithm wherein we reduce the audio quality by cutting off certain frequencies, that are not sensitive to the human ear, and also decrease the rate at which the frequencies are read by the computer (sampling rate).  
The audio compression can be run by using the following command   
```python audioCompress.py``` 
### Image Compression Algorithm
The image compression algorithm works by the qoi lossless compression algorithm. It converts a raw image file to qoi format. Which is 50 - 60 times faster than png

```ts-node compression.ts```
