##
 #  Worg
 ##

word_list = ["papagal", "pisica","soarece","bolovan","soparla","catel", "pasare"]

def generate_matrix():
    matrix = []

    row = ['#']
    for i in range(0, 26):
        row.append(chr(ord('a') + i))
    matrix.append(row)

    for i in range(0, 26):
        row = []
        row.append(chr(ord('a') + i))

        for j in range(0, 26):
            row.append(0)

        matrix.append(row)

    return matrix



def print_matrix(matrix):
    for i in range(len(matrix)):
        row = ""
        for j in range(len(matrix[i])):
            row = row + str(matrix[i][j])
            row = row + " "
        print(row)



def fill_matrix(matrix, word_list):
    for word in word_list:
        for i in range(len(word) - 1):
            matrix[1 + ord(word[i]) - ord('a')][1 + ord(word[i + 1]) - ord('a')] += 1



def delete_empty_rows(matrix):
    to_delete = []
    for i in range(1, len(matrix)):
        counter = 0
        for j in range(1, len(matrix[i])):
            if matrix[i][j] != 0:
                counter += 1

        if counter == 0:
            to_delete.append(i)

    to_delete.reverse()
    for row_id in to_delete:
        matrix.pop(row_id)



def delete_empty_columns(matrix):
    to_delete = []
    for i in range(1, len(matrix[0])):
        counter = 0
        for j in range(1, len(matrix)):
            if matrix[j][i] != 0:
                counter += 1

        if counter == 0:
            to_delete.append(i)

    to_delete.reverse()

    for i in range(0, len(matrix)):
        for column_id in to_delete:
            matrix[i].pop(column_id)


matrix = generate_matrix()
fill_matrix(matrix, word_list)
delete_empty_rows(matrix)
delete_empty_columns(matrix)
print_matrix(matrix)
