from hashlib import md5

class LotteryDrawing(object):
    
    def __init__(self):
        self.date = None
        self.numbers = None
        self.special_numbers = None
        self.description = ""
        
    def match(numberString):
        pass
    
    def hash(self):
        hash_str = "{}{}{}".format(self.date, self.numbers, self.special_numbers)
        return md5(hash_str.encode()).hexdigest()
    
    def number_string(self):
        
        num_str = ""
        for i in range(len(self.numbers)):
            num_str += str(self.numbers[i])
            
            if i != len(self.numbers)-1:
                num_str += "-"
                
        if self.special_numbers:
            num_str += " {}".format(self.special_numbers[0])
                
        return num_str
    
    def __repr__(self):
        return "{} {} {}".format(self.date, self.numbers, self.special_numbers)

class Lottery(object):
    
    def __init__(self):
        self.name = "Base Lottery Parser"
        self.states_available = None
        self._drawings = []
        
    def get_drawings(self):
        pass
    
    @property
    def drawings(self):
        return self.get_drawings()

    def has_drawing_today(self):
        return False
