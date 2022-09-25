#!/usr/bin/env python
import sys
import os
import utils.videoMode as videoMode

def hasXrandrRotation():
    with open("/usr/share/batocera/batocera.arch") as fb:
        arch = fb.readline().strip()
    return arch in ['x86_64', 'x86']
    
def isVerticalScreen(system):
    return system.getOptString("display.rotate") in ["1", "3"];

def isFbneoVerticalScreen(system):
    return system.name == "fbneo" and isVerticalScreen(system)

def shouldHandleRotation(system):
    return system.isOptSet("display.rotate") and (not hasXrandrRotation())

def setFbneoVerticalMode(system, coreSettings):
    if (shouldHandleRotation(system) and isFbneoVerticalScreen(system)):
        if (system.config["display.rotate"] == "1"):
            coreSettings.save('fbneo-vertical-mode', 'enabled')
        elif (system.config["display.rotate"] == "3"):
            coreSettings.save('fbneo-vertical-mode', 'alternate')
    else:
        coreSettings.save('fbneo-vertical-mode', 'disabled')
        
def shouldSetLibretroAspectRatio(system):
    return shouldHandleRotation(system) and isVerticalScreen(system) and system.name != "fbneo"        

def setLibretroAspectRatioForVerticalScreen(system, rom, retroarchConfig):
    if system.name == 'mame':
        isVerticalGame = videoMode.getAltDecoration('mame', rom, 'retroarch')
        if isVerticalGame == "0":
            retroarchConfig['aspect_ratio_index'] = '8'
        else:
            retroarchConfig['aspect_ratio_index'] = '0'
    else:
        retroarchConfig['aspect_ratio_index'] = '8'
    retroarchConfig['video_aspect_ratio_auto'] = 'false'    
            