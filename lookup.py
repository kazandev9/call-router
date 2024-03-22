#first_format   +14146072404
#second_format  414-607-2404
#third_format   14146072404
#fourth_format  +1 (414)607-2404

from hubspot_contacts import get_props_from_number

class lookup:
    def __init__(self, from_number):
        self.from_number = from_number
        self.formats = {
            "first": self.from_number,
            "second": self.dash_format(),
            "third": self.third_format(),
            "fourth": self.fourth_format(),
            "fifth": self.fifth_format(),
        }
        
        
    #go through lookup results and determine which one is right
    #ideally, most should be none, but its not always consistent
    def get_right_contact(self):
        non_none = []
        lookups = self.preform_lookups()
        for result in lookups:
            if lookups[result] is not None:
                non_none.append(lookups[result])
        if len(non_none) == 1:
            return  non_none[0]
        else:
            return non_none
            
        
    def preform_lookups(self):
        #initalize the return object
        results = {"first": None, "second": None, "third": None, "fourth": None, "fifth": None}
        for key in self.formats:
            #print(self.formats[key])
            lookup_result = get_props_from_number(self.formats[key])
            #print(lookup_result)
            if lookup_result not in results.values():
                results[key] = lookup_result
        return results
        
    
    def dash_format(self):
        return f"{self.from_number[2:5]}-{self.from_number[5:8]}-{self.from_number[8:]}"
    
    def third_format(self):
        return self.from_number[1:]
    
    def fourth_format(self):
        return f"{self.from_number[0:2]} ({self.from_number[2:5]}){self.from_number[5:8]}-{self.from_number[8:]}"
    
    def fifth_format(self):
        return f" {self.dash_format()}"
    
    def __str__(self):
        ret = ""
        for key in self.formats.keys():
            ret += f"{key}: {self.formats[key]}\n"
        return ret
        

