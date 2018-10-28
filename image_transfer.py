import os, sys, time

def swap(fname,destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data

def image_capture(fnameout):
    cmd = 'raspistill -o '+fnameout
    os.system(cmd)
    os.system('git add '+fnameout)
    os.system('git commit -m "Automated ImagePostage"')
    os.system('push origin HEAD:master')


def main():
    if len(sys.argv) < 2:
        exit(0)
    else:
        fname = sys.argv[1] 
        image_capture(fname)
