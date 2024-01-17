import pandas as pd 
product_list = pd.read_excel('inventory.xlsx' , 'Sheet1')
columns= list(product_list.columns)
suppliers = set(list(product_list[columns[3]]))
list_suppliers=list(suppliers)
list_suppliers.sort()
product_count = len(list(product_list[columns[0]]))
product_per_supplier = {list_suppliers[i-1]: 0 for i in range(1,len(suppliers)+1)}
inventory_per_supplier = {list_suppliers[i-1]: 0 for i in range(1,len(suppliers)+1)}
product_no_under_10= []
product_inv_under_10 = []



print(product_per_supplier)
for index in range(1,product_count+1):
    product_per_supplier[list(product_list[columns[3]])[index-1]] +=1
    inventory_per_supplier[list(product_list[columns[3]])[index-1]] +=list(product_list[columns[1]])[index-1] * list(product_list[columns[2]])[index-1]
    if(list(product_list[columns[1]])[index-1] < 10):
        product_no_under_10.append(list(product_list[columns[0]])[index-1])
        product_inv_under_10.append(list(product_list[columns[1]])[index-1])

product_under_10 = {product_no_under_10[i]: product_inv_under_10[i] for i in range(len(product_no_under_10))}


# All Required Data
print(product_per_supplier) 
print(inventory_per_supplier)
print(product_under_10)