
from io import StringIO
import sys

class Hider:
    def __init__(self, channels=('stdout',)):
        self._stomach = StringIO()
        self._orig = {ch : None for ch in channels}

    def __enter__(self):
        for ch in self._orig:
            self._orig[ch] = getattr(sys, ch)
            setattr(sys, ch, self)
        return self

    def write(self, string):
        self._stomach.write(string)

    def flush(self):
        pass

    def autopsy(self):
        return self._stomach.getvalue()

    def __exit__(self, *args):
        for ch in self._orig:
            setattr(sys, ch, self._orig[ch])



def file_parser(sourcefile,targetfile):
    with open ('fileerrorlog.txt','w') as el:
        print('starting error log\n')
    with open(sourcefile,'r') as f:
    	j=500000
    	l=[]
    	k=0
    	while k < j:
            try:
                row=f.readline()
                l.append(row)
                k+=1
            except Exception as ex:
                print(ex)
                with open ('fileerrorlog.txt','a') as el:
                    el.write('line: '+str(k)+' : '+str(ex)+'\n')
                pass
    real_len=len(set(l))

    with open(targetfile,'w') as f:
        for i in l[0:real_len]:
            f.write(i)

if __name__=='__main__':
    sourcefile=input("Enter name of file to check: ")
    print('\n')
    targetfile=input("Enter target filename: ")
    print('\n')
    with Hider() as h:
        file_parser(sourcefile,targetfile)
