from json import JSONEncoder
from evaluate import evaluate

class LogJsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Log():
    def __init__(self, jsonFile):
        self.log = []
        self.jsonFile = jsonFile
    def add(self, entry):
        self.log.append(entry)
    def asJson(self):
        return LogJsonEncoder().encode(self.log)
    def writeJson(self):
        handle = open(self.jsonFile, "w")
        handle.seek(0)
        handle.write(self.asJson())
        handle.close()

class LogEntry():
    def __init__(self, sampleName, originalName, detectedMimeType, jfifVersion, binwalk, fileHeader, foremost, fileSize, diffColorDRgb):
        self.sampleName = sampleName
        self.originalName = originalName
        self.detectedMimeType = detectedMimeType
        self.blindAttribs = {
            "jfifVersion": {
                "attribTool": "exiftool",
                "data": jfifVersion,
                "result": evaluate("jfifVersion", jfifVersion)
            },
            "binwalkData": {
                "attribTool": "binwalk",
                "data": binwalk,
                "result": evaluate("binwalkData", binwalk)
            },
            "fileHeader": {
                "attribTool": "strings",
                "data": fileHeader,
                "result": evaluate("fileHeader", fileHeader)
            },
            "foremostCarving": {
                "attribTool": "foremost",
                "data": foremost,
                "result": evaluate("foremostCarving", foremost)
            }
        }
        if fileSize != None or diffColorDRgb != None:
            self.nonBlindAttribs = {
                "fileSize": {
                    "attribTool": "exiftool",
                    "data": fileSize,
                    "result": evaluate("fileSize", fileSize)
                },
                "colorMeanDifference": {
                    "attribTool": "stegoveritas, imagemagick",
                    "data": diffColorDRgb,
                    "result": evaluate("colorMeanDifference", diffColorDRgb)
                }
            }
