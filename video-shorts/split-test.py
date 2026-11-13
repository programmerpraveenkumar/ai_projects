def split_string_by_length(string):
    for i in range(0,len(string),5):
        return [string[i:i + 5] for i in range(0, len(string), 5)]

# Example usage:
input_string = "abcdefghijklmnopqrstuvwxyz"
result = split_string_by_length(input_string)
print(result)
for i in result:
    print(i)
# print(result)  
