# Ứng dung:
# Duy trì trạng thái: Khi bạn muốn tạo một hàm ghi nhớ trạng thái giữa các lần gọi
# Hàm tạo hàm: Khi muốn tạo các hàm động dựa trên tham số truyền vào
# Callback và xử lý sự kiện: Trong trường hợp gọi hàm callback thì closure sẽ giúp giữ lại các biến cần thiết

# ----------------------------------------------
# Hàm tạo hàm
def outer_function(x):
    def inner_function(y):
        return x + y

    # Return the inner function as a result of the outer function execution
    return inner_function


# Create a closure
new_closure = outer_function(5)
# Now, new_closure have x = 5
# Call the closure with y = 10
print(new_closure(10))

# ----------------------------------------------
# Duy trì trạng thái
def counter():
    count = 0

    def increment():
        nonlocal count # Cho phép thay đổi biến bên ngoài
        count += 1
        return count

    return increment

# Create a closure
counter_closure = counter()
print(counter_closure())
print(counter_closure())
print(counter_closure())

# ----------------------------------------------
# Callback và xử lý sự kiện
def on_btn_click(message):
    def callback():
        print("Button clicked! " + message)

    return callback
# Create a closure
example_close = on_btn_click('Click Zo')
example_close()
