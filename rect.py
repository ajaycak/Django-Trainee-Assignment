class Rectangle:
    def __init__(self,length:int , width:int):

        if not isinstance(length, int) or not isinstance(width, int):
            raise TypeError("Length and width must be integers")

        self.length= length
        self.width = width
        
    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}  
    
