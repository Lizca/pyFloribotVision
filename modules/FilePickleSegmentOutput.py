#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
#Author: Björn Eistel
#Contact: <eistel@gmail.com>
#
# THIS SOURCE-CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO EVENT WILL 
# THE AUTHOR BE HELD LIABLE FOR ANY DAMAGES ARISING FROM THE USE OF THIS SOURCE-CODE. USE AT YOUR OWN RISK.


from BaseModule import BaseModule
import cv2
import logging
import pickle
import numpy as np


class FilePickleSegmentOutput(BaseModule):
    obligatoryConfigOptions = {'inputImageName': None, 'inputContourName': None, 'inputContourIndexListName': None,
                               'outputFile': None, 'overwriteExistingFile': None, 'createFilePath': None,
                               'cacheCycles': None, 'skipDump': None}

    def __init__(self, **kwargs):
        super(type(self), self).__init__(**kwargs)
        self.log = logging.getLogger(__name__)
        self.log.debug('logging started')

    def postOptActions(self):
        self.pickleCycleCntr = 0
        self.pickleCache = list()
        self.dataFile = open(self.outputFile, 'wb')
        self.skipDump = True if self.skipDump == 'True' else False


    def externalCall(self):
        self.cacheCycles = int(self.cacheCycles)

        self.appendOutputDataToCache()

        if self.cacheCycles is not -1 and self.pickleCycleCntr >= self.cacheCycles:
            self.writeCacheToFile()
            self.pickleCycleCntr = -1
        self.pickleCycleCntr += 1

    def preOptActions(self):
        self.writeCacheToFile()
        self.dataFile.close()

    def appendOutputDataToCache(self):
        image = self.ioContainer[self.inputImageName]
        cont = self.ioContainer[self.inputContourName]
        if self.inputContourIndexListName in self.ioContainer:
            contidx = self.ioContainer[self.inputContourIndexListName]
        else:
            contidx = range(len(cont))

        self.ioContainer[self.inputImageName]

        #create

        shape = list(image.shape[0:2])
        #shape = list(image.shape)
        shape.insert(0, len(contidx))
        shape = tuple(shape)

        ccimage = np.zeros(shape, np.uint8)

        for k, v in enumerate(contidx):
            cv2.drawContours(ccimage[k], cont, v, (255, 255, 255), -1)

        singleImageDump = list()
        #each found segment in image
        for segmentid, segmentcnt in enumerate(ccimage):

            shapePointList = list()
            for shapepoint in cont[contidx[segmentid]]:
                x = shapepoint[0][0]
                y = shapepoint[0][1]
                shapePointList.append([x, y])

            segmentObjPoints = list()
            pixlist = np.nonzero(segmentcnt)
            for xk, y in enumerate(pixlist[0]):
                x = pixlist[1][xk]
                #segmentObjPoints.append([x, y])
                segmentObjPoints.append([x, y, image[y][x][2], image[y][x][1], image[y][x][0]])

            singleImageDump.append([shapePointList, segmentObjPoints])

        #if len(singleImageDump) > 0:
        self.pickleCache.append(image)
        self.pickleCache.append(singleImageDump)


    def writeCacheToFile(self):
        if self.skipDump:
            self.log.debug('writeCacheToFile method is skipped')
            return

        #ToDo: create directory if not exist and allowed
        #print 'chache length', len(self.pickleCache)

        #directory = os.path.dirname(self.outputFile)

        #if not os.path.exists(directory):
        #    os.makedirs(directory)

        cnt = 2
        cntmax = len(self.pickleCache)
        objectDumpNames = ['raw-image', 'segments']
        self.log.debug('dump %d frames to file <%s>', cntmax, self.outputFile)
        for data in self.pickleCache:

            self.log.debug('Frame %d of %d (%s)', cnt / 2, cntmax / 2, objectDumpNames[cnt % 2])
            pickle.dump(data, self.dataFile)
            cnt += 1
        print
        self.pickleCache = list()



