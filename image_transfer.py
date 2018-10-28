import os, sys, time
import RPi.GPIO as GPIO


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data


def image_capture(fnameout):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22,GPIO.OUT)
    GPIO.output(22,GPIO.HIGH) 
    try:
        cmd = 'raspistill -o remoteImagery/' + fnameout
        os.system(cmd)
        os.system('git add remoteImagery/' + fnameout)
        os.system('git commit -m "Automated ImagePostage"')
        os.system('git push origin HEAD:master')
    except:
        os.system('python cleanup_gpio.py')


def main():
    if len(sys.argv) < 2:
        exit(0)
    else:
        fname = sys.argv[1] 
        image_capture(fname)
        GPIO.output(22,GPIO.LOW)
        GPIO.cleanup()


if __name__ == '__main__':
    main()

