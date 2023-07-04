# def accum(s):
#     return "-".join((c * i).title() for i, c in enumerate(s, 1))
#
#
# print(accum("abcd"))
# print(accum("RqaEzty"))
#
#
# def to_alternating_case(string):
#     # return "".join([char.upper() if char.islower() else char.lower() for char in string])
#     return string.swapcase()
#
# print(to_alternating_case("hello world"))

# def wave(people):
#     result = []
#
#     people_list = [char for char in people]
#
#     for i in range(len(people_list)):
#         if people_list[i] != " ":
#             result.append("".join(people_list[:i]) + people_list[i].upper() + "".join(people_list[i + 1:]))
#
#     return result
#
#
# print(wave("hello"))
# print(wave("two words"))
#
# def points(games):
#     result = 0
#
#     for score in games:
#         if score[0] > score[2]:
#             result += 3
#         elif score[0] == score[2]:
#             result += 1
#
#     return result
#
#
# print(points(['1:0', '2:0', '3:0', '4:0', '2:1', '3:1', '4:1', '3:2', '4:2', '4:3']))
#
# def is_isogram(string):
#     for c in string.lower():
#         if string.lower().count(c) > 1:
#             return False
#     return True
#
#
# print(is_isogram("Dermatoglyphics"))
# print(is_isogram("isogram"))
# print(is_isogram("moOse"))
#
# def binary_array_to_number(arr):
#     return int("".join(str(c) for c in arr), 2)
#
#
# print(binary_array_to_number([0, 0, 0, 1]))
# print(binary_array_to_number([0, 0, 1, 0]))
# print(binary_array_to_number([0, 1, 0, 1]))
# print(binary_array_to_number([1, 0, 0, 1]))
#
# def likes(names):
#     likes_this = " likes this"
#     like_this = " like this"
#
#     if len(names) == 0:
#         return "no one" + likes_this
#
#     if len(names) == 1:
#         return names[0] + likes_this
#
#     if len(names) == 2:
#         return names[0] + " and " + names[1] + like_this
#
#     if len(names) == 3:
#         return names[0] + ", " + names[1] + " and " + names[2] + like_this
#
#     if len(names) > 3:
#         return names[0] + ", " + names[1] + " and " + f"{len(names) - 2} others" + like_this
#
#
# print(likes([]))
# print(likes(["Peter"]))
# print(likes(["Jacob", "Alex"]))
# print(likes(["Max", "John", "Mark"]))
# print(likes(["Alex", "Jacob", "Mark", "Max"]))
# def duplicate_encode(word):
#     # result = ""
#     # for char in word.lower():
#     #     if word.lower().count(char) == 1:
#     #         result += "("
#     #     else:
#     #         result += ")"
#
#     return "".join(["(" if word.lower().count(char) == 1 else ")" for char in word.lower()])
#
# print(duplicate_encode("din"))
# print(duplicate_encode("recede"))
# print(duplicate_encode("Success"))
# print(duplicate_encode("(( @"))
#
# def order(sentence):
#     result = sentence.split()
#     for word in sentence.split():
#         for char in word:
#             try:
#                 result.pop(int(char) - 1)
#                 result.insert(int(char) - 1, word)
#             except BaseException:
#                 continue
#     return " ".join(result)
#
#
# print(order("is2 Thi1s T4est 3a"))
# print(order("4of Fo1r pe6ople g3ood th5e the2"))
#
# def find_difference(a, b):
#     def find_mul(lst):
#         mul_a = 1
#
#         for i in lst:
#             mul_a *= i
#         return mul_a
#
#     return find_mul(a) - find_mul(b)
#
#
# print(find_difference([3, 2, 5], [1, 4, 4]))

def oddity(n):
    result = []

    for i in range(1, n + 1):
        if n % i == 0:
            result.append(i)

    return "even" if sum(result) % 2 == 0 else "odd"


print(oddity(12))
print(oddity(4))
