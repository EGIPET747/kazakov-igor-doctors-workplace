import datetime
import threading
import os
import queue


def input_file():
    global in_queue, out_queue
    while True:
        try:
            path = in_queue.get()
            print(f'path = {path}')
            if not path:
                break
            in_file = open(path[0], 'r')
            file_text = in_file.read()
            out_queue.put((file_text, path[0]))
            in_file.close()
            in_queue.task_done()
        except:
            in_queue.task_done()
            print('...ERROR_INPUT...')
            continue


def output_file():
    global result
    while True:
        try:
            out_file = open(r'OUT_FILE\OUT_FILE.txt', 'a')
            num = result.get()
            print(f'num = {num}')
            out_file.write(f'File \'{num[1]}\' ; SUM = {num[0]}\n')
            out_file.close()
            print(f'closed {num}')
            result.task_done()
        except:
            result.task_done()
            print('...err out done...')


def handler():
    global out_queue, result
    while True:
        sum = 0
        text = out_queue.get()
        for line in text[0].strip().split('\n'):
            line = line.strip().split()
            for num in line:
                try:
                    sum += float(num)
                except:
                    print('...ERROR_HANDLER...')
                    continue
        result.put((str(sum), text[1]))
        out_queue.task_done()
        print(f'end {sum}')


start = datetime.datetime.now()
folder = 'IN_FILES'
path = os.path.abspath(os.curdir)
full_path = f'{path}\\{folder}'
files = os.listdir(full_path)
in_queue = queue.Queue()
out_queue = queue.Queue()
result = queue.Queue()

res = []
# out = open(r'OUT_FILE\OUT_FILE_LINE.txt', 'a')
for file in files:

    in_queue.put((f'{full_path}\\{file}', file))
    print((f'{full_path}\\{file}', file))
    # file = open(f'{full_path}\\{file}', 'r')
    # file_text = file.read()
    # file.close()
    # sum = 0
    # for line in file_text.strip().split('\n'):
    #     line = line.strip().split()
    #     for num in line:
    #         sum += float(num)
    # out.write(f'File \'{full_path}\\{file}\' ; SUM = {sum}\n')
# out.close()
print(f'LINEAR = {datetime.datetime.now() - start}')
print(f'THREADED = 0:00:03:597450')

start = datetime.datetime.now()

read = threading.Thread(target=input_file, daemon=True)
calculate = threading.Thread(target=handler, daemon=True)
write = threading.Thread(target=output_file, daemon=True)
read.start()
calculate.start()
write.start()


print(1)
read.join()
print(2)
calculate.join()
print(3)
write.join()
print(datetime.datetime.now() - start)
