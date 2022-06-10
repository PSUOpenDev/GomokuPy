import sys
MAX_INT = sys.maxsize

class GomokuAction:
    Point = tuple([int,int])
    
    def __init__(self,player_id:int, point: Point):
        self.__id = player_id
        self.__x = point[0]
        self.__y = point[1]
        self.__hash:int = self.__id * (self.__x + self.__y + 1)

    def hash(self)->int:
        return self.__hash

    def get_x(self)->int:
        return self.__x

    def get_y(self)->int:
        return self.__y

    def get_id(self)->int:
        return self.__id

    def get_point(self)->Point:
        return (self.__x,self.__y)