import pdb

print '''
+ - - - - - - - - +
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
+ - - - - - - - - + '''


class SudokuContentBase:
    pass


class SudokuRows(SudokuContentBase):
    pass


class SudokuColumns(SudokuContentBase):
    pass


class SudokuBox():
    pass


class Sudoku():
    def __init__(self):
        self.question_list = []
        self.all_value_set_dict = {}
    
    def read_content_from_file(self):
        with open('question.txt', 'r') as fp:
            question_file_rows_list = fp.readlines()
        return question_file_rows_list
    
    def get_question_content_in_list(self):
        question_file_rows_list = self.read_content_from_file()

        for question_file_rows in question_file_rows_list:
            self.question_list.append(question_file_rows.split(','))

    only_number_list = []
    aa = []
    all_numbers_set = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

    def get_proper_list(self, content_list, list_type=None):
        # pdb.set_trace()
        for row in self.question_list:
            content_list.append([0 if not x.strip() else int(x) for x in row])

    def get_valid_counts(content_list, list_type):
        for index, row in enumerate(content_list):
            if row.count(0) == 0:
                ALL_VALUE_SET_DICT[list_type][0][index] = 1
    
    
    def set_counts():
        get_valid_counts(all_rows, "rows")
        get_valid_counts(all_cols, "cols")
        get_valid_counts(all_box, "box")
    
    
    def fill_the_only_missing_number(all_common_list, list_type):
        (all_rows, all_cols, all_box) = ALL_VALUE_SET_DICT["rows"][1], ALL_VALUE_SET_DICT["cols"][1], \
                                        ALL_VALUE_SET_DICT["box"][1]
        for rindex, temp_list in enumerate(all_common_list):
            if temp_list.count(0) == 1:
                # pdb.set_trace()
                list_of_numbers = [val for val in temp_list if val]
                value = list(all_numbers_set - set(list_of_numbers))[0]
                cindex = temp_list.index(0)
                set_values_in_all_lists(all_rows, all_cols, all_box, rindex, cindex, value, list_type)
    
    
    def set_values_in_all_lists(all_rows, all_cols, all_box, rindex, cindex, value, list_type):
        # pdb.set_trace()
        if list_type == "rows":
            index1, index2 = rindex, cindex
            all_box[int(rindex / 3) * 3 + int(cindex / 3)][(rindex % 3) * 3 + cindex % 3] = value
        if list_type == "cols":
            index1, index2 = cindex, rindex
            all_box[int(cindex / 3) * 3 + int(rindex / 3)][(cindex % 3) * 3 + rindex % 3] = value
        if list_type == "box":
            all_box[rindex][cindex] = value
            index1 = (int(rindex / 3) * 3) + cindex / 3
            index2 = (rindex % 3) * 3 + int(cindex % 3)
    
        only_number_list[index1][index2] = value
        all_rows[index1][index2] = value
        all_cols[index2][index1] = value
        if list_type == "box":
            index1 = rindex
        ALL_VALUE_SET_DICT[list_type][0][index1] = 1
    
    
    def solve_sudoku():
        while True:
            if 0 not in ALL_VALUE_SET_DICT["rows"][0]:
                break
            for key in ALL_VALUE_SET_DICT.keys():
                fill_the_only_missing_number(ALL_VALUE_SET_DICT[key][1], key)
            set_counts()
    
    
    def print_sudoku(content_list):
        for val in content_list:
            print val
        print "\n\n"
    
    
    all_rows = only_number_list
    print_sudoku(all_rows)
    
    all_cols = map(list, zip(*only_number_list))
    print_sudoku(all_cols)
    
    # pdb.set_trace()
    temp = []
    all_box = []
    for row in range(0, 3):
        for col in range(0, 3):
            for i in range(0, 9):
                temp.append(only_number_list[int(i / 3) + (row * 3)][i % 3 + (col * 3)])
            all_box.append(temp)
            temp = []
    
    print_sudoku(all_box)
    
    ALL_VALUE_SET_DICT = {
        "rows": ([0, 0, 0, 0, 0, 0, 0, 0, 0], all_rows),
        "cols": ([0, 0, 0, 0, 0, 0, 0, 0, 0], all_cols),
        "box": ([0, 0, 0, 0, 0, 0, 0, 0, 0], all_box)
    }
    
    # pdb.set_trace()
    solve_sudoku()
    print_sudoku(only_number_list)


    def start(self):
        self.get_question_content_in_list()
        self.get_proper_list(only_number_list)
        pass



def main():
    sudoku_obj = Sudoku()
    sudoku_obj.start()


if __name__ == "__main__":
    main()
