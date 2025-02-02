# Decorators là một hàm nhận hàm khác làm tham số
# Cho phép thay đổi, mở rộng mà không làm thay đổi mã nguồn của hàm đó.
# Thường được thêm các chức năng như logging, kiểm tra điều kiện thực thi, thời gian thực hiện hàm, ...

# Cú pháp ----------------------------------------------------
def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        # Thực hiện các thao tác trước khi gọi hàm gốc
        result = original_function(*args, **kwargs)
        # Thực hiện các thao tác sau khi gọi hàm gốc
        return result

    return wrapper_function
# -------------------------------------------------------------
# Để sử dụng thì chỉ cần thêm @name_decorator vào trước hàm cần gọi đến
@decorator_function
def example_func(a, b):
    return a + b
print(example_func(1, 2))

print('-------------------------------------------------------------')
# Add logging
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        print(f'Calling function: {func.__name__}')
        result = func(*args, **kwargs)
        print(f'Function returned: {result}')
        return result
    return wrapper

@logger_decorator
def greet(name_title):
    print(name_title)

greet('Add logger!')
print('-------------------------------------------------------------')
# Measure execution time
import time
def ex_time_decorator(func):
    def wrapper(*args, **kwargs):
        print(f'Calling function: {func.__name__}')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'Execution time: {end_time - start_time} seconds')
        return result
    return wrapper

@ex_time_decorator
def sample_func(n):
    time.sleep(n)

sample_func(1)
print('-------------------------------------------------------------')
# Check condition before execute function
def check_condition_decorator(func):
    def wrapper(*args, **kwargs):
        role = kwargs.get('role', 'guest')
        print(role)
        if role == "admin":
            print('Condition is true, executing function...')
            result = func(*args, **kwargs)
            print('Function executed successfully.')
            return result
        print('Condition is false, skipping function...')
        return 'Access denied'
    return wrapper
@check_condition_decorator
def sample_check(role=None, guest=None):
    return 'Data accessed'

sample_check(role='admin')
sample_check(guest='OK')
sample_check(role='user')

print('-------------------------------------------------------------')
# Check cache of function
def check_cache_decorator(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            print('Returning cached function')
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@check_cache_decorator
def expensive_computation(x):
    print("Performing expensive operation")
    return x * x

print(expensive_computation(5))
print(expensive_computation(5))
print(expensive_computation(6))
print('-------------------------------------------------------------')
# Authentication
def authentication_decorator(func):
    def wrapper(*args, **kwargs):
        auth = kwargs.get('token')
        if auth == 'authentication':
            return func(*args, **kwargs)
        print('Authentication failed')
        return 'Authentication failed'
    return wrapper

@authentication_decorator
def secure_data(token=None):
    print('Authentication successful')

secure_data(token='authentication')
secure_data()
print('-------------------------------------------------------------')
# Retry function
def retry_decorator(max_retries=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    print(f"Retry {retries}/{max_retries} after error: {e}")
                    time.sleep(1)
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator

@retry_decorator(max_retries=3)
def unreliable_function():
    import random
    if random.random() < 0.7:
        raise Exception("Something went wrong")
    return "Success"

print(unreliable_function())