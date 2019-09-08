mylist = ['this','is','a','list','Ture']
mydic = {'one':1,'two':2,'three':3,'four':4,'five':5}
print('列表所有元素和类型',mylist,type(mylist))
print('字典所有元素和类型',mydic,type(mydic))
print('列表切片后的显示：',mylist[0:5:2])
print('列表追加元素：',mylist.append('False'),mylist)
print('列表删除元素：',mylist.pop(4),mylist)
mylist[0]='there'
print('列表修改元素：',mylist)
