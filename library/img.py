"""The Img module for use with frontend - allows for image color processing"""

from __future__ import division #so we don't have to worry about int division
import Image, sys
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats #for distribution

class Img(object):
    """Allows for processing and displaying image information"""
    
    def __init__(self, filename):
        """Initializes an image from a filename - generates histograms"""
        self.im = Image.open(filename).convert("RGB")
        #split the image into into RGB bands
        self.bands = self.im.split()
        for self.color in range(3):
            self.hist = self.bands[self.color].histogram()
            self.generateHist("library/" + str(self.color) + "pre.jpg")
        

    def run(self, values, method):
        """processes the image - takes values to adjust, string method"""
        self.center = values
        self.method = method
        print "Processing..."
        for self.color in range(3):
            if (self.center[self.color] != 0):
                out = self.process()
            self.hist = self.bands[self.color].histogram()
            self.generateHist("library/" + str(self.color) + "post.jpg")

        #merge image
        self.im = Image.merge("RGB", self.bands)
        self.im.save("library/out.jpg")
        print("Done")
  
    def findAverage(self, lis):
        """args - a list with index color, value frequency returns average color"""
        sumcolor = 0
        sumpixels = 0
        for i in range(0, len(lis)-1):
            sumcolor += i*lis[i]
            sumpixels += lis[i]
        return sumcolor / sumpixels        

    def generateHist(self, name):
        """generates histograms"""
        plt.close()
        x = []
        for i in range(0, 255):
            for j in range(0, self.hist[i]):
                x.append(i)

        hist, bins = np.histogram(x, bins = 50)
        width = 2
        center = (bins[:-1]+bins[1:])/2
        plt.xlim((0, 256))
        plt.bar(center, hist, align = 'center', width = width)
        plt.savefig(name)

    def process(self):
        """processes the image - in place"""
        if (self.method == "N"):
            histStats = scipy.stats.norm(self.center[self.color], 40)
            count = 0
            for i in range(0, len(self.hist)):
                count += self.hist[i]
            self.results = []
            update = 0
            for i in range(0, len(self.hist)):
                update += (self.hist[i] / count)
                temp = min(255, max(0, histStats.ppf(update)))
                self.results.append(temp)
            out = self.bands[self.color].point(lambda i: self.results[i])
        else:
            out = self.bands[self.color].point(lambda i: min(255, max(0, i + self.center[self.color])))

        self.bands[self.color].paste(out)


