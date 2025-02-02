# Tạo ra các hàm ẩn danh (anonymous function)
# Thường được kết hợp với map(), filter(), sorted()
# -> lambda arguments : expression

# ---------------------------------------------------
# Sử dụng cùng map()
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
squares = list(map(lambda x : x**2, numbers))
print(squares)

# ---------------------------------------------------
# Sử dụng cùng filter()
numbers = [1, 2, 3, 4, 5, 6]
even_numb = list(filter(lambda x : x%2 == 0, numbers))
print(even_numb)

# ---------------------------------------------------
# Sử dụng cùng sorted()
pairs = [(2, 5), (1, 8), (3, 0), (8, 1), (0, 9)]
sorted_list = sorted(pairs, key=lambda x : x[0])
print(sorted_list)