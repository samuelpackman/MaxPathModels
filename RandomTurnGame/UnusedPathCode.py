def updatePathArrayAt(self,index):
      ind1 = index[0]
      ind2 = index[1]
      if ind1 == self.size - 1: #last row in body array
          self.pathArray[ind1][ind2] = [Path(self.body[ind1][ind2], [], [ind1,ind2], self.size,[[ind1,ind2]])]
      else:
          PathListChoice1 = self.pathArray[ind1 + 1][ind2]
          PathListChoice2 = self.pathArray[ind1 + 1][ind2 + 1]
          pathScoreDiff = PathListChoice1[0].score - PathListChoice2[0].score
          if pathScoreDiff > 0: #straight path is better
              self.pathArray[ind1][ind2] = [Path(self.body[ind1][ind2] + pathChoice.score, [0] + pathChoice.path, [ind1,ind2], self.size, [[ind1,ind2]] + pathChoice.pathList) for pathChoice in PathListChoice1]
          elif pathScoreDiff < 0:
              self.pathArray[ind1][ind2] = [Path(self.body[ind1][ind2] + pathChoice.score, [1] + pathChoice.path, [ind1,ind2], self.size, [[ind1,ind2]] + pathChoice.pathList) for pathChoice in PathListChoice2]
          else:
              self.pathArray[ind1][ind2] = [Path(self.body[ind1][ind2] + pathChoice.score, [0] + pathChoice.path, [ind1,ind2], self.size, [[ind1,ind2]] + pathChoice.pathList) for pathChoice in PathListChoice1] + [Path(self.body[ind1][ind2] + pathChoice.score, [1] + pathChoice.path, [ind1,ind2], self.size, [[ind1,ind2]] + pathChoice.pathList) for pathChoice in PathListChoice2]

  def updateWholePathArray(self):
      for ind1 in range(self.size - 1, -1, -1):
          for ind2 in range(ind1 + 1):
              self.updatePathArrayAt([ind1,ind2])

  def updatePathArrayFrom(self,index): #updates whole array starting at index
      for i in range(index[0]-index[1],-1,-1):
          for j in range(index[1],-1,-1):
              self.updatePathArrayAt([i+j,j])

  def updatePathArrayFindBestPathScore(self):
      self.updateWholePathArray()
      return self.pathArray[0][0].score

  def updatePathArrayFindBestPathPath(self):
      self.updateWholePathArray()
      return self.pathArray[0][0].path

  def setAndUpdate(self,index,value):
      if self.body[index[0]][index[1]] == value:
          pass
      else:
          self.body[index[0]][index[1]] = value
          self.updatePathArrayFrom(index)
