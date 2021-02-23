import os, schedule, time, re
from win10toast import ToastNotifier

toast = ToastNotifier()
icopath = r'C:\Users\yuyuichiu\Desktop\Python_stuff\Shutdown_Scheduler\clock.ico'
#C:\Users\yuyuichiu\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

def shutdown():
    global called
    if not called:
        os.system('shutdown -s -t 60')    #shutdown computer -s
        toast.show_toast('Shutdown Alert',
                            'Your computer will shutdown in 60s, prepare yourself to work.',
                            icon_path = icopath,
                            duration = 60,
                            threaded = True)
        called = True

def countdown(timing: str):
    msg = 'Your computer will shutdown after ' + timing + ' minutes. '
    toast.show_toast('Shutdown Preparation Alert',
                        msg,
                        icon_path = icopath,
                        duration = 60,
                        threaded = True)

def softcountdown(timing: str):
    msg = 'Your computer will do a one-time shutdown after ' + timing + ' minutes. '
    toast.show_toast('Soft Shutdown Preparation Alert',
                        msg,
                        icon_path = icopath,
                        duration = 60,
                        threaded = True)

def start_reminder():
    toast.show_toast('Shutdown Scheduler is Active.',
                        'Just a reminder :>',
                        icon_path = icopath,
                        duration = 60,
                        threaded = True)

if __name__ == '__main__':
    called = False
    rawtime = time.asctime(time.localtime())
    ftime = re.findall('..:..:..',rawtime)
    hour = int(ftime[0][0:2])
    minute = int(ftime[0][3:5])

    schedule.every().day.at('22:00').do(countdown, timing = '30')
    schedule.every().day.at('22:15').do(countdown, timing = '15')
    schedule.every().day.at('22:25').do(countdown, timing = '5')
    schedule.every().day.at('22:29').do(countdown, timing = '1')
    schedule.every().day.at('22:30').do(shutdown)

    schedule.every().day.at('15:45').do(countdown, timing = '15')
    schedule.every().day.at('15:55').do(countdown, timing = '5')
    schedule.every().day.at('15:59').do(countdown, timing = '1')
    schedule.every().day.at('16:00').do(shutdown)

    start_reminder()
    while True:
        schedule.run_pending()
        if (hour == 22 and minute >= 30) or (hour == 23) or (hour == 0 and minute < 30): #22:30 to 0:30
            shutdown()
        time.sleep(1)
