# def greet(**kwargs):
#     print(kwargs)
#
# greet(name='Alice', age=25)
#
# def create_dict(**kwargs):
#     return kwargs
#
# result = create_dict(a=1, b=2, c=3)
# print(result)
#
# def update_settings(default_settings, **kwargs):
#     default_settings.update(kwargs)
#     return default_settings
#
# default_settings = {
#     "theme": "light",
#     "notifications": True
# }
# result = update_settings(
#     default_settings,
#     theme="dark",
#     volume=80
# )
# print(result)

# def filter_kwargs(**kwargs):
#     result = {}
#     for key, value in kwargs.items():
#         if value > 10:
#             result[key] = value
#     return result
#
# print(filter_kwargs(a=5, b=20, c=15, d=3))
#
# def my_function(**kwargs):
#     print(f"Called with kwargs: {kwargs}")
#
# my_function(debug=True, verbose=False)

# def log_kwargs(func):
#     def wrapper(*args, **kwargs):
#         print(f"Called with kwargs: {kwargs}")        # строка которую ты уже написала
#         return func(*args, **kwargs)
#     return wrapper
#
# @log_kwargs
# def my_function(a, b, **kwargs):
#     return a + b
#
# my_function(5, 10, debug=True, verbose=False)

# def add_numbers(*args):
#     return sum(args)
# print(add_numbers(1, 2, 3))
# print(add_numbers(10, 20, 30, 40))

# def create_list(*args):
#     list = []
#     for data in args:
#         list.append(data)
#     return list
#
# print(create_list(1, "apple", True, 3.14))

# def pass_arguments(*args):
#     return print_args(*args)
# def print_args(*args):
#     for arg in args:
#         print(arg)

# def find_max(*args):
#     return max(args)
#
# print(find_max(10, 20, 5, 100, 50))

# def join_strings(*args):
#     return ' '.join(args)
# print(join_strings("Hello", "world", "!"))

# def process_data(*args, **kwargs):
#     print(f'Positional arguments: {args}')
#     print(f'Keyword arguments: {kwargs}')
#
# process_data(1, 2, 3, name="Alice", age=25)

# def configure_function(*args, **kwargs):
#     return kwargs
#
# print(configure_function("theme", "volume", theme="dark", volume=50))

# def log_args_kwargs(func):
#     def wrapper(*args, **kwargs):
#         print(f'Positional arguments: {args}')
#         print(f'Keyword arguments: {kwargs}')
#         return func(*args, **kwargs)
#     return wrapper
#
# @log_args_kwargs
# def my_function(x, y, **kwargs):
#     return x + y
#
# my_function(10, 20, debug=True, verbose=False)
#
# result = my_function(10, 20, debug=True, verbose=False)
# print(result)

def est():
    yield 1
    yield 2

g = est()

print(next(g))
print(next(g))
