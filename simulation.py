import csv, argparse, sys

class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def tick(self):
        if self.current_request != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_request = None

    def busy(self):
        if self.current_request != None:
            return True
        else:
            return False

    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.get_time()

class Request:
    def __init__(self, request):
        self.request_time = int(request[0])
        self.process_time = int(request[2])

    def get_stamp(self):
        return self.request_time

    def get_time(self):
        return self.process_time

    def wait_time(self,current_time):
        return current_time - self.process_time

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self,item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

def get_nxt_server(server_queue):
    server = server_queue.dequeue()
    
    while server.busy():
        server.tick()
        server_queue.enqueue(server)
        server = server_queue.dequeue()
    return server

def simulateManyServers(file, server_count):
    reqs_queue = Queue()
    server_queue = Queue()
    wait_times = []
    prev_time = 0

    for line, row in enumerate(csv.reader(file)):
        request = Request(row)
        reqs_queue.enqueue(request)

    i = 0
    while i < server_count:
        server_queue.enqueue(Server())
        i += 1

    while not reqs_queue.is_empty():
        server = get_nxt_server(server_queue)
        
        if not server.busy() and not reqs_queue.is_empty():
            next_request = reqs_queue.dequeue()
            current_time = request.get_stamp()
            wait_times.append(next_request.wait_time(current_time))
            server.start_next(next_request)
            prev_time = next_request.request_time
        
        server.tick()
        server_queue.enqueue(server)

    avg_wait_time = sum(wait_times) / len(wait_times)
    print("Avg wait: %3.1f seconds" % avg_wait_time)

def simulateOneServer(file):
    server = Server()
    reqs_queue = Queue()
    wait_times = []
    prev_time = 0

    for line, row in enumerate(csv.reader(file)):
        request = Request(row)
        reqs_queue.enqueue(request)

    while not reqs_queue.is_empty():
        if not server.busy() and not reqs_queue.is_empty():
            next_request = reqs_queue.dequeue()
            current_time = request.get_stamp()
            wait_times.append(next_request.wait_time(current_time))
            server.start_next(next_request)
            prev_time = next_request.request_time
        server.tick()

    avg_wait_time = sum(wait_times) / len(wait_times)
    print("Avg wait: %3.1f secondss" % avg_wait_time)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='CSV file with request inputs', type=str)
    parser.add_argument('--servers', help='Number of servers for simulation', type=int)
    args = parser.parse_args()

    if args.file:
        try:
            inputs_data = open(args.file)
        except:
            print('Error reading CSV file.')
            sys.exit()

        if args.servers and args.servers > 1:
            simulateManyServers(inputs_data, args.servers)
        elif not args.servers or (args.servers and args.servers <= 1):
            simulateOneServer(inputs_data)

    else:
        print('File paramenter requiered. Usage: python simulation.py --file PATH_TO_FILE')
        sys.exit()

if __name__ == '__main__':
    main()