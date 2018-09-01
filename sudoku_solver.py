from copy import deepcopy
from collections import namedtuple


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
        new_question_list = deepcopy(question_list)
        self.set_data(new_question_list)
        self.update_counts()

    def set_data(self, new_question_list):
        raise NotImplementedError("set_data method needs to be defined")

    def update_counts(self):
        for index, row in enumerate(self.all_data_for_type_list_list):
            if row.count(0) == 0:
                # Updates if line of sudoku type is yet to be filled
                self.unfilled_entries_list[index] = True


class SudokuRows(SudokuContentBase):
    def __init__(self, question_list):
        SudokuContentBase.__init__(self, question_list)

    def set_data(self, new_question_list):
        # All rows are already arranged as necessary
        self.all_data_for_type_list_list = new_question_list

    @staticmethod
    def get_sudoku_type():
        return "rows"


class SudokuColumns(SudokuContentBase):
    def __init__(self, question_list):
        SudokuContentBase.__init__(self, question_list)

    def set_data(self, new_question_list):
        # construct a transpose of existing question list
        self.all_data_for_type_list_list = map(list, zip(*new_question_list))

    @staticmethod
    def get_sudoku_type():
        return "cols"


class SudokuBox(SudokuContentBase):
    def __init__(self, question_list):
        SudokuContentBase.__init__(self, question_list)

    def set_data(self, new_question_list):
        # construct a transpose of existing question list
        temp = []
        all_box = []
        for row in range(0, 3):
            for col in range(0, 3):
                for i in range(0, 9):
                    # Iterate through question list to construct a list containing content of a box
                    temp.append(new_question_list[int(i / 3) + (row * 3)][i % 3 + (col * 3)])
                all_box.append(temp)
                temp = []
        self.all_data_for_type_list_list = all_box

    @staticmethod
    def get_sudoku_type():
        return "box"


class SudokuSolver:
    def __init__(self):
        self.answer_list = []
        self.all_type_obj_named_tuple = namedtuple("type_obj", ["rows_obj", "cols_obj", "box_obj"])
        self.all_type_obj = None

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

    def fill_the_only_missing_number(self):
        for type_obj in self.all_type_obj:
            line_type = type_obj.get_sudoku_type()
            all_numbers_list_list = type_obj.all_data_for_type_list_list
            for row_index, line_list in enumerate(all_numbers_list_list):
                if line_list.count(0) == 1:
                    # Proceed further only if there is one entry with 0 in a line
                    list_of_numbers = [val for val in line_list if val]
                    value = list(ALL_NUMBERS_SET - set(list_of_numbers))[0]
                    col_index = line_list.index(0)
                    self.update_missing_value_in_all_types(row_index, col_index, value, line_type)
                    type_obj.update_counts()
    
    def update_missing_value_in_all_types(self, row_index, col_index, value, list_type):
        # Updates each of the separate list if any one of the empty row has been correctly
        # filled
        (rows_obj, cols_obj, box_obj) = self.all_type_obj.rows_obj, self.all_type_obj.cols_obj,\
                                        self.all_type_obj.box_obj
        if list_type == "rows":
            index1, index2 = row_index, col_index
            box_obj.all_data_for_type_list_list[int(row_index / 3) * 3 + int(col_index / 3)][(row_index % 3) * 3 + col_index % 3] = value
        if list_type == "cols":
            index1, index2 = col_index, row_index
            box_obj.all_data_for_type_list_list[int(col_index / 3) * 3 + int(row_index / 3)][(col_index % 3) * 3 + row_index % 3] = value
        if list_type == "box":
            box_obj.all_data_for_type_list_list[row_index][col_index] = value
            index1 = (int(row_index / 3) * 3) + col_index / 3
            index2 = (row_index % 3) * 3 + int(col_index % 3)
    
        # only_number_list[index1][index2] = value
        rows_obj.all_data_for_type_list_list[index1][index2] = value
        cols_obj.all_data_for_type_list_list[index2][index1] = value
        # if list_type == "box":
        #     index1 = row_index

    def solve_sudoku(self):
        # list_type = type_obj.get_sudoku_type()
        self.fill_the_only_missing_number()

    def print_sudoku(self):
        print "\n\n\n"
        for val in self.all_type_obj.rows_obj.all_data_for_type_list_list:
            print val
        print "\n\n\n"

    @staticmethod
    def get_have_all_lines_been_filled(type_obj):
        print type_obj.unfilled_entries_list
        return all(type_obj.unfilled_entries_list)

    # print_sudoku(all_box)
    # # pdb.set_trace()
    # solve_sudoku()
    # print_sudoku(only_number_list)

    def start(self):
        print "Process Begins"
        question_list = self.get_question_list()
        rows_obj = SudokuRows(question_list)
        cols_obj = SudokuColumns(question_list)
        box_obj = SudokuBox(question_list)

        self.all_type_obj = self.all_type_obj_named_tuple(rows_obj, cols_obj, box_obj)

        # self.sudoku_line_type_object_tuple = (rows_obj, cols_obj, box_obj)
        count = 0
        self.print_sudoku()
        while True:
            count += 1
            print "Try %s" % count
            # Can pass any object to this function, result is expected to be the same
            # Passing row_obj here
            all_lines_filled = self.get_have_all_lines_been_filled(rows_obj)
            if all_lines_filled:
                self.print_sudoku()
                break
            self.solve_sudoku()


def main():
    sudoku_obj = SudokuSolver()
    sudoku_obj.start()


if __name__ == "__main__":
    main()
