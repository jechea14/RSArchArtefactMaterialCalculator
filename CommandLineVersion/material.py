# Create class to store material data
class Materials:
    def __init__(self, mat_name, mat_amount, mat_price, total_mat_price):
        self._mat_name = mat_name
        self._mat_amount = int(mat_amount)
        self._mat_price = int(mat_price)
        self._total_mat_price = int(total_mat_price)
        
    @property
    def MatName(self):
        return self._mat_name
    
    @property
    def MatAmount(self):
        return self._mat_amount
    
    @property
    def MatPrice(self):
        return self._mat_price

    @property
    def TotalMatPrice(self):
        return self._total_mat_price
    
    @MatAmount.setter
    def MatAmount(self, mat_amount):
        self._mat_amount = mat_amount

    @TotalMatPrice.setter
    def TotalMatPrice(self, total_mat_price):
        self._total_mat_price = total_mat_price