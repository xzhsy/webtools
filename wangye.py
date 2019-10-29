from bs4 import BeautifulSoup
import os,sys

print(os.getcwd())
filepath=os.path.join('F:\\小车','b.html')
with open(filepath,'r',encoding='utf-8') as f:
    content = f.read()
    f.close()

format = BeautifulSoup(content,"html.parser")

# print(format.contents)
# # print(format.find_all('tr'))
for i in format.find_all('tr',class_="ivu-table-row"):
    # a = i.attrs
    print(i)
    alist=[]
    for m in i.find_all('span'):
        # print(m.string)
        alist.append(m.string)
    print(alist)
# with open('a.txt','a') as f:
#     f.write(i)
#     f.close()
# # print(type(i.stripped_strings))
# for f in i.stripped_strings:
#     print(f)