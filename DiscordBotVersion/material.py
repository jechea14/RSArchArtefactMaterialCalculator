# Create class to store material data
class Materials:
    def __init__(self, mat_name, mat_amount, mat_price, total_mat_price):
        self._mat_name = mat_name
        self._mat_amount = int(mat_amount)
        self._mat_price = int(mat_price)
        self._total_mat_price = int(total_mat_price)
        
    @property
    def mat_name(self):
        return self._mat_name
    
    @property
    def mat_amount(self):
        return self._mat_amount
    
    @property
    def mat_price(self):
        return self._mat_price

    @property
    def total_mat_price(self):
        return self._total_mat_price
    
    @mat_amount.setter
    def mat_amount(self, mat_amount):
        self._mat_amount = mat_amount

    @total_mat_price.setter
    def total_mat_price(self, total_mat_price):
        self._total_mat_price = total_mat_price