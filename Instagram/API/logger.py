from datetime import date, datetime
def log(tag='', message=''):
    path = 'logs/log_' + str(date.today()) + '.txt'
    file = open(path, 'a')
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    file.write(f'{now} {tag}: {message}\n')

def log_add_task(message: str):
    log('Instagram', message)