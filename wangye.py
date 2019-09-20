from bs4 import BeautifulSoup
import os,sys

print(os.getcwd())
filepath=os.path.join('F:\\小车','a.html')
with open(filepath,'r',encoding='utf-8') as f:
    content = f.read()
    f.close()

format = BeautifulSoup(content,"html.parser")

print(format.name)
for i in format.attrs:
    print(i)