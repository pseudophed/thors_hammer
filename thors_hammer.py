#!/usr/bin/python3.4
#written by pseudophed (The Great)
# o7 bitches #

import urllib.request, datetime, argparse, queue, threading, multiprocessing

parser = argparse.ArgumentParser(prog='thors_hammer', description='Load test web sites or web applications')
parser.add_argument('-u', action='store', dest='url', required=True)
parser.add_argument('-n', action='store', type=int, dest='total_requests', help='Total requests to make to the server. Default is 10')
parser.add_argument('-c', action='store', type=int, dest='conc_conn', help='Total number of concurrent connections to make')
parser.add_argument('-v', action='version', version='%(prog)s 1.0')
commandArgs = parser.parse_args()

requests = multiprocessing.Queue()
q = multiprocessing.JoinableQueue()
total_reqs = -5


def load_test():
    
    while not q.empty():
        if q.qsize() % 1000 == 0:
            print('{} requests left to perform...'.format(q.qsize()))
        testUrl = q.get()
#        print(testUrl)
        try:
            response = urllib.request.urlopen(testUrl)
            response.readall()
            requests.put('whoop')
            #print(requests)
        except Exception as err:
#            print(err)
            pass
        
        #print(requests.qsize())
        q.task_done()
 
def load_queue(queueSize, testUrl):

    for x in range(queueSize):
        q.put(testUrl)
    #q.close()
    #print(q.qsize())

def run():
    
    if commandArgs.total_requests:
        total_requests = commandArgs.total_requests
    else:
        total_requests = 10    
    
    print('Load testing {}:'.format(commandArgs.url))    
    load_queue(total_requests, commandArgs.url)
    
#    print('q.qsize: {}'.format(q.qsize()))
    
    if commandArgs.conc_conn:
        concurrent = commandArgs.conc_conn
    else:
        concurrent = 1

    for a in range(concurrent):
        p = multiprocessing.Process(target=load_test)
#        p.daemon = True
        p.start()
        
    p.join()

#    print('run loop: {}'.format(requests.qsize()))

def main():
    
    startTime = datetime.datetime.now()
    
    run()    

#    print('main loop: {}'.format(requests.qsize()))
    
    print('Processed {} successful requests out of {} requests performed ({}% success rate) in {} seconds.'.format(requests.qsize(), commandArgs.total_requests,str((requests.qsize()/commandArgs.total_requests) * 100),str((datetime.datetime.now() - startTime).total_seconds())))



if __name__ == '__main__' :
    main()