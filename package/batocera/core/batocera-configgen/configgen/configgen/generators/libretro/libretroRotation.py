#!/usr/bin/env python
import sys
import os
import utils.videoMode as videoMode

def hasXrandrRotation():
    with open("/usr/share/batocera/batocera.arch") as fb:
        arch = fb.readline().strip()
    return arch in ['x86_64', 'x86']
    
def isVerticalScreen(system):
    return system.getOptString("display.rotate") in ["1", "3"]

def isVerticalGame(system, rom):
    if (not (system.name == "mame" or system.name == "fbneo")):
        return false
    if (not system.isOptSet("__isVerticalGame__")):
        altDecoration = videoMode.getAltDecoration('mame', rom, 'retroarch')
        system.config['__isVerticalGame__'] = (altDecoration != "0")
    return system.config['__isVerticalGame__']        

def handleRotationInLibretroConfig(system, rom, retroarchConfig):
    if (hasXrandrRotation()):
        return
    isVertGame = isVerticalGame(system, rom)
    rotationOption = "0"
    if (system.isOptSet("display.rotate")):
        rotationOption = system.getOptString("display.rotate")
    if (rotationOption == "0"):
        retroarchConfig["video_rotation"] = "3" if isVertGame else "0"
    if (rotationOption == "1"):
        retroarchConfig["video_rotation"] = "2" if isVertGame else "3"
    if (rotationOption == "2"):
        retroarchConfig["video_rotation"] = "1" if isVertGame else "2"
    if (rotationOption == "3"):
        retroarchConfig["video_rotation"] = "0" if isVertGame else "1"     

def setFbneoVerticalMode(system, rom, coreSettings):
    if ((not hasXrandrRotation()) and isVerticalGame(system, rom) and system.name == "fbneo"):
        coreSettings.save('fbneo-vertical-mode', 'alternate')
    else:
        coreSettings.save('fbneo-vertical-mode', 'disabled')

def setMame2003PlusTateMode(system, rom, coreSettings):
    if ((not hasXrandrRotation()) and isVerticalGame(system, rom)):
        coreSettings.save('mame2003-plus_tate_mode', 'enabled')
    else:
        coreSettings.save('mame2003-plus_tate_mode', 'disabled')

def shouldSetLibretroAspectRatio(system, rom):
    isVertScreen = isVerticalScreen(system)
    isVertGame = isVerticalGame(system, rom)
    return not (hasXrandrRotation() or ((not isVertScreen) and (not isVertGame)) or (isVertScreen and isVertGame))       

def setLibretroAspectRatioForRotation(system, rom, retroarchConfig):
    retroarchConfig['aspect_ratio_index'] = '8'   

def setMameCommandLineForRotation(system, rom, commandLine):
    if isVerticalGame(system, rom):
        commandLine += ['-autorol']  

def handleVerticalShader(system, rom):
    isVertScreen = isVerticalScreen(system)
    isVertGame = isVerticalGame(system, rom)
    if (((not isVertScreen) and isVertGame) or (isVertScreen and (not isVertGame))):
        if "shaderset" in system.config:
            if system.config["shaderset"] != "none":
                vertShaderSet = system.config["shaderset"] + "-vertical"
                if os.path.exists("/userdata/shaders/configs/" + vertShaderSet + "/rendering-defaults.yml") or os.path.exists("/usr/share/batocera/shaders/configs/" + vertShaderSet + "/rendering-defaults.yml"):
                    system.config["shaderset"] = vertShaderSet          