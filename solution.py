import argparse
from collections import defaultdict
import os
import sys


class RenderFarmParser(object):
    """
    A class that processes render farm data
    """

    def __init__(self, path):
        self.path = path
        # Add a check for valid path
        # Main counters
        self.render_success_count = 0
        self.render_failure_count = 0

        # Average counters
        self.avg_time = 0
        self.avg_ram = 0
        self.avg_cpu = 0

        # Max counters
        self.max_ram_id = ""
        self.max_ram = 0
        self.max_cpu = 0
        self.max_cpu_id = ""

        # Counter dictionaries
        self.app_counter = defaultdict(int)
        self.renderer_counter = defaultdict(int)

    def _count(self, filename):
        """
        Count success and failure per file
        :param filename: Filename to open and count success for
        :return:
        """
        with open(filename, 'r') as f:
            for line in f:
                if line != '\n':
                    is_success = line.split(',')[4] == 'true'
                    ids = line.split(',')[0]
                    app_name = line.split(',')[1]
                    renderer = line.split(',')[2]
                    time = line.split(',')[5]
                    ram = line.split(',')[6]
                    cpu = line.split(',')[7]
                    if is_success:
                        self.app_counter[app_name] += 1
                        self.renderer_counter[renderer] += 1
                        self.render_success_count += 1
                        self.avg_time += float(time)
                        self.avg_ram += float(ram)
                        self.avg_cpu += float(cpu)

                        if float(ram) > self.max_ram:
                            self.max_ram = float(ram)
                            self.max_ram_id = ids
                        if float(cpu) > self.max_cpu:
                            self.max_cpu = float(cpu)
                            self.max_cpu_id = ids

                    else:
                        self.render_failure_count += 1

    def process(self):
        """
        Entrypoint method that starts processing all CSV files in a
        given path
        :return:
        """
        for filename in os.listdir(self.path):
            if filename.endswith('.csv'):
                self._count(filename)

    def summary(self):
        # print (self.render_success_count)
        # print (self.render_failure_count)
        print (int((self.avg_time / self.render_success_count)/1000))
        print (self.avg_cpu / self.render_success_count)
        print (self.avg_ram / self.render_success_count)
        print (self.max_ram_id)
        print (self.max_cpu_id)



def main():
    parser = argparse.ArgumentParser(description='Render farm parser.')
    parser.add_argument('-path', metavar='P', type=str, help='path to csv files')
    parser.add_argument('-app', type=str, help='filter with app name')
    parser.add_argument('-renderer', type=str, help='filter with renderer')
    parser.add_argument("-failed",action='store_true', help='output the failed renderers')
    parser.add_argument('-summary',action='store_true', help='use -summary summary')
    parser.add_argument('-avgtime', action='store_true',help='use -avgtime avgtime')
    parser.add_argument('-avgcpu', action='store_true', help='use -avgcpu avgcpu')
    parser.add_argument('-avgram', action='store_true', help='use -avgram avgram')
    parser.add_argument('-maxram', action='store_true', help='use -maxram maxram')
    parser.add_argument('-maxcpu', action='store_true', help='use -maxcpu maxcpu')
    args = parser.parse_args()
    if args.path:
        render_farm_parser = RenderFarmParser(args.path)
    else:
        render_farm_parser = RenderFarmParser(os.getcwd())
    render_farm_parser.process()
    print(render_farm_parser.render_success_count)

    if args.app:
        print(render_farm_parser.app_counter[args.app])
    if args.renderer:
        print(render_farm_parser.renderer_counter[args.renderer])
    if args.avgtime:
        print (int((render_farm_parser.avg_time / render_farm_parser.render_success_count)/1000))
    if args.avgcpu:
        print(render_farm_parser.avg_cpu / render_farm_parser.render_success_count)
    if args.avgram:
        print(render_farm_parser.avg_ram / render_farm_parser.render_success_count)
    if args.maxram:
        print(render_farm_parser.max_ram_id)
    if args.maxcpu:
        print(render_farm_parser.max_cpu_id)
    if args.summary:
        render_farm_parser.summary()
    if args.failed:
        print(render_farm_parser.render_failure_count)

        # print ("Success count is ", render_farm_parser.render_success_count)
        # print ("Failure count is ", render_farm_parser.render_failure_count)
        # print ("Avg Time ", render_farm_parser.avg_time / render_farm_parser.render_success_count)
        # print ("Avg Ram ", render_farm_parser.avg_ram / render_farm_parser.render_success_count)
        # print ("Avg Cpu ", render_farm_parser.avg_cpu / render_farm_parser.render_success_count)
        # print ("Id with Max CPU usage is",render_farm_parser.max_cpu_id)
        # print ("Id with Max Ram usage is",render_farm_parser.max_ram_id)


if __name__ == '__main__':
    main()

