
class AutoVectorDBUpdater:
    def __init__(self) -> None:
        self.chunkUnit = 10
        pass

    def updateGroupVectorDB(self, groupId):
        point = self.getLatestUpdatedPoint(groupId)
        dataForUpdate = self.getDataForUpdate(groupId, point)
        
        for i in range(0, len(dataForUpdate), self.chunkUnit):
            if i + self.chunkUnit > len(dataForUpdate):
                break
            self.updateVectorDB(groupId, dataForUpdate[i:i+self.chunkUnit])
        
    def updateVectorDB(self, groupId, dataForUpdate):
        pass

    def getLatestUpdatedPoint(self, groupId):
        return 0
    
    def getDataForUpdate(self, groupId, point):
        return 0
