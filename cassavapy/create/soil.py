import os
import re


class Soil(object):

    def __init__(self, soil_id):
        self.id = soil_id
        self.folder = "C:/DSSAT47/Soil/"
        self.params = {"ICLB": [], "SH20": []}

        self._start()

    def _start(self):

        self.soil_lines = []
        [self._read_file(n) for n in os.scandir(self.folder) if not self.soil_lines]

        self._read_params()

    def _read_file(self, file):

        with open(file.path) as f:
            section = []
            for i, l in enumerate(f.readlines()):

                if l[0] == '!':  # skip comments
                    continue

                if l[0] == '*':  # start of section

                    if l[1:].split()[0] == self.id:
                        self._extract_soil_lines(file, self.id, i)
                        break

    def _extract_soil_lines(self, file, soil_id, line):

        with open(file.path) as f:
            for i, l in enumerate(f.readlines()):
                if i >= line:

                    if l[0] == "!" or len(l) == 1:
                        continue
                    if self.soil_lines and l[0] == "*":
                        break

                    self.soil_lines.append(l)

    def _read_params(self):

        for l in self.soil_lines:
            if l[0] == "@":

                if "SLB" in l.split():
                    depth = re.search("(SLB)", l).end()
                    lower = re.search("(SLLL)", l).end()
                    upper = re.search("(SDUL)", l).end()
                    continue
            try:
                self.params["ICLB"].append(int(l[depth - 2:depth]))
                tot_water = float(l[upper - 4:upper]) - float(l[lower - 4:lower])
                self.params["SH20"].append(round(tot_water, 3))
            except:
                pass
