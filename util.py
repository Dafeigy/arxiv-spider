import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class MTDownloader():
    '''
    Using Multi-thread to download file(s).
    
    Multi thread are recommand for big file download(`file_size`>50Mb).

    Usage:
    ```python
        target_url = 'https://issuepcdn.baidupcs.com/issue/netdisk/yunguanjia/Baidunetdisk_7.24.1.2.exe'
        file_name = 'Baidunetdisk_7.24.1.2.exe'
        dl = MTDownloader(num_thread=12)
        dl(target_url, file_name)
    ```
    '''
    def __init__(self,num_thread:int=6) -> None:
        self.num_thread = num_thread
        self.record=[]
        

    def down(self, start, end, chunk_size=1024):
        headers = {'range':f'bytes={start}-{end}'}
        res = requests.get(self.url, headers=headers, stream=True)
        with open(self.name, "rb+") as f:
            f.seek(start)
            for chunk in res.iter_content(chunk_size):
                f.write(chunk)
                self.downloaded_size += chunk_size

    def main(self):
        start_time = time.time()
        f = open(self.name, 'wb')
        f.truncate(self.file_size)
        f.close()
        tp = ThreadPoolExecutor(max_workers=self.num_thread)
        futures = []
        start = 0
        for i in range(self.num_thread):
            end = int((i+1)/self.num_thread*self.file_size)
            future = tp.submit(self.down, start, end)
            futures.append(future)
            start = end+1
        while True:
            process = self.downloaded_size/self.file_size*100
            last = self.downloaded_size
            time.sleep(1)
            curr = self.downloaded_size
            down = (curr-last)/1024
            if down > 1024:
                speed = f'{down/1024:6.2f}MB/s'
            else:
                speed = f'{down:6.2f}KB/s'
            print(f'process: {process:6.2f}% | speed: {speed}', end='\r')
            self.record.append([process, down])
            if process >= 100:
                print(f'process: {100.00:6}% | speed:  00.00KB/s', end=' | ')
                break
        tp.shutdown()
        end_time = time.time()
        total_time = end_time-start_time
        average_speed = self.file_size/total_time/1024/1024
        print(f'total-time: {total_time:.0f}s | average-speed: {average_speed:.2f}MB/s | Thread-nums:{self.num_thread}')

    def __call__(self, url:str,file_name:str):
        self.name = file_name
        self.url = url
        self.head = requests.head(self.url, allow_redirects=True)
        self.file_size = int(self.head.headers['Content-Length'])
        self.downloaded_size = 0
        self.main()

if __name__ =="__main__":
    dl = MTDownloader(12)
    dl('https://arxiv.org/e-print/2001.00008','2001.00008.tar.gz')
    print(dl.record)


    