import math


class Tracker:
    def __init__(self):       
        self.centerPoints = {}
        self.idCount = 0
    
    def Euclidean(self, objects, distanceOfPoints):
        objectsIDs = []
        for (x, y, w, h) in objects:
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            
            sameObject = False
            for id, pt in self.centerPoints.items():
                dist = math.hypot(cx - pt[0], cy - pt[1]) #Returns a float value having Euclidean norm, sqrt(x*x + y*y).
                if dist < distanceOfPoints:
                    self.centerPoints[id] = (cx, cy)
                    objectsIDs.append([x,y,w,h, id])
                    sameObject = True
                    break

            if sameObject is False:
                self.centerPoints[self.idCount] = (cx, cy)
                objectsIDs.append([x,y,w,h, self.idCount])
                self.idCount += 1
                
        newCenterPoints = {}
        for objectsID in objectsIDs:
            _, _, _, _, newID = objectsID
            center = self.centerPoints[newID]
            newCenterPoints[newID] = center
        
        self.centerPoints = newCenterPoints.copy()
        return objectsIDs