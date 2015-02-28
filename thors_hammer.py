#!/usr/bin/python3.4
#written by pseudophed (The Great)
# o7 bitches #

import concurrent.futures, urllib.request, datetime, argparse, queue, threading

parser = argparse.ArgumentParser(prog='thors_hammer', description='Load test web sites or web applications')
parser.add_argument('-u', action='store', dest='url', required=True)
parser.add_argument('-n', action='store', type=int, dest='total_requests', help='Total requests to make to the server. Default is 10')
parser.add_argument('-c', action='store', type=int, dest='conc_conn', help='Total number of concurrent connections to make')
parser.add_argument('-v', action='version', version='%(prog)s 1.0')
commandArgs = parser.parse_args()

#commandArgs.dest = 'http://www.weepyadmin.com'

requests = 0
q = queue.Queue()

def load_test():
    while not q.empty():
        if q.qsize() % 1000 == 0:
            print('{} requests left to perform...'.format(q.qsize()))
        global requests
        testUrl = q.get_nowait()
        try:
            response = urllib.request.urlopen(testUrl)
            response.readall()
            #print(requests)
            requests += 1
        except Exception as err:
            print(err)
            pass
        q.task_done()
 
def load_queue(queueSize, testUrl):
    global q
    for x in range(queueSize):
        q.put(testUrl)
    #print(q.qsize())

def run():

    if commandArgs.total_requests:
        total_requests = commandArgs.total_requests
    else:
        total_requests = 10    
    
    print('Load testing {}:'.format(commandArgs.url))    
    load_queue(total_requests, commandArgs.url)
    #load_test()
    
    if commandArgs.conc_conn:
        concurrent = commandArgs.conc_conn
    else:
        concurrent = 1
        
    for i in range(concurrent):
        t = threading.Thread(target=load_test)
        t.daemon = True
        t.start()
        
    q.join()

def main():
    
    startTime = datetime.datetime.now()
    
    run()

    print('Processed {} requests in {} seconds.'.format(requests, str((datetime.datetime.now() - startTime).total_seconds())))






if __name__ == '__main__' :
    main()