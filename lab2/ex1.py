import sys

def aduna(*args):
    answer = 0
    for x in args:
        try:
            answer += int(x)
        except Exception as error:
            print("Nu toate argumentele sunt numere")
            sys.exit(0)

    return answer

arg_list = []
for i in range(1, len(sys.argv)):
    arg_list.append(sys.argv[i])

print(aduna(*arg_list))
