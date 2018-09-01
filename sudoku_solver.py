from copy import deepcopy


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


ALL_NUMBERS_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9}


class SudokuContentBase:

    def __init__(self, question_list):
        self.unfilled_entries_list = [False]*9
        self.all_data_for_type_list_list = []
        answer_list = deepcopy(question_list)
        self.set_data(answer_list)

    def set_data(self, question_list):
        raise NotImplementedError("set_data method needs to be defined")

    def update_counts(self, content_list):
        for index, row in enumerate(content_list):
            if row.count(0) == 0:
                # Updates if line of sudoku type is yet to be filled
                self.unfilled_entries_list[index] = True



class SudokuRows(SudokuContentBase):
    def __init__(self, question_list):
        SudokuContentBase.__init__(self, question_list)

    def set_data(self, question_list):
        # All rows are already arranged as necessary
        self.all_data_for_type_list_list = question_list

    @staticmethod
    def get_sudoku_type():
        return "rows"


class SudokuColumns(SudokuContentBase):
    def __init__(self, question_list):
        SudokuContentBase.__init__(self, question_list)

    def set_data(self, question_list):
        # construct a transpose of existing question list
        self.all_data_for_type_list_list = map(list, zip(*question_list))

    @staticmethod
    def get_sudoku_type():
        return "columns"


class SudokuBox(SudokuContentBase):
    def __init__(self, question_list):
        SudokuContentBase.__init__(self, question_list)

    def set_data(self, question_list):
        # construct a transpose of existing question list
        temp = []
        all_box = []
        for row in range(0, 3):
            for col in range(0, 3):
                for i in range(0, 9):
                    # Iterate through question list to construct a list containing content of a box
                    temp.append(question_list[int(i / 3) + (row * 3)][i % 3 + (col * 3)])
                all_box.append(temp)
                temp = []
        self.all_data_for_type_list_list = all_box

    @staticmethod
    def get_sudoku_type():
        return "boxes"


class SudokuSolver:
    def __init__(self):
        self.answer_list = []


    @staticmethod
    def get_question_list():
        question_list = list()
        content_list = list()

        with open('question.txt', 'r') as fp:
            question_file_rows_list = fp.readlines()
            for question_file_rows in question_file_rows_list:
                content_list.append(question_file_rows.split(','))

            for row in content_list:
                # Converting string to int
                question_list.append([0 if not x.strip() else int(x) for x in row])

        return question_list

    def fill_the_only_missing_number(self, **kwargs):
        for type_obj in kwargs.values():
            if type_obj.all_data_for_type_list_list.count(0) == 1:
                # Proceed further only if there is a entry with 0 in line
                list_of_numbers = [val for val in temp_list if val]
                value = list(all_numbers_set - set(list_of_numbers))[0]
                cindex = temp_list.index(0)
                set_values_in_all_lists(all_rows, all_cols, all_box, rindex, cindex, value, list_type)
        type_obj.update_counts()
    
    
    def set_values_in_all_lists(all_rows, all_cols, all_box, rindex, cindex, value, list_type):
        # Updates each of the separate list if any one of the empty row has been correctly
        # filled
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
        self.all_values_set_dict[list_type][0][index1] = 1

    def solve_sudoku(self, **kwargs):
        # list_type = type_obj.get_sudoku_type()
        self.fill_the_only_missing_number(**kwargs)

    
    
    def print_sudoku(content_list):
        for val in content_list:
            print val
        print "\n\n"

    @staticmethod
    def get_have_all_lines_been_filled(type_obj):
        return all(type_obj.unfilled_entries_list)

    
    print_sudoku(all_box)
    # # pdb.set_trace()
    # solve_sudoku()
    # print_sudoku(only_number_list)

    def start(self):
        question_list = self.get_question_list()
        rows_obj = SudokuRows(question_list)
        cols_obj = SudokuColumns(question_list)
        box_obj = SudokuBox(question_list)
        # self.sudoku_line_type_object_tuple = (rows_obj, cols_obj, box_obj)
        while True:
            # Can pass any object to this function, result is expected to be the same
            # Passing row_obj here
            all_lines_filled = self.get_have_all_lines_been_filled(rows_obj)
            if all_lines_filled:
                break
            self.solve_sudoku(rows_obj=rows_obj, cols_obj=cols_obj, box_obj=box_obj)



def main():
    sudoku_obj = SudokuSolver()
    sudoku_obj.start()


if __name__ == "__main__":
    main()
