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


class SudokuCell:
    def __init__(self, value, row_index, col_index):
        self.possible_values_in_cell = set()
        self.possible_row_values = set()
        self.possible_col_values = set()
        self.possible_box_values = set()
        self.rows_row_index = row_index
        self.rows_col_index = col_index
        self.cols_row_index = col_index
        self.cols_col_index = row_index
        self.box_row_index = int(row_index / 3) * 3 + int(col_index / 3)
        self.box_col_index = (row_index % 3) * 3 + col_index % 3
        self.value = value

        if not self.value:
            # value is empty, this cell needs to be solved, find all possibilities
            self.set_possible_values_for_cell()

    def set_possible_values_for_cell(self):
        import pdb; pdb.set_trace()
        self.possible_row_values = ALL_NUMBERS_SET - set(SudokuRows.ROWS_LIST[self.rows_row_index])
        self.possible_col_values = ALL_NUMBERS_SET - set(SudokuColumns.COLS_LIST[self.cols_row_index])
        self.possible_box_values = ALL_NUMBERS_SET - set(SudokuBox.BOX_LIST[self.box_row_index])


class SudokuRows:
    ROWS_LIST = []

    def __init__(self):
        pass

    @classmethod
    def set_data(cls, new_question_list):
        # All rows are already arranged as necessary
        cls.ROWS_LIST = new_question_list

    @staticmethod
    def get_sudoku_type():
        return "rows"


class SudokuColumns:
    COLS_LIST = []

    def __init__(self):
        pass

    @classmethod
    def set_data(cls, new_question_list):
        # construct a transpose of existing question list
        cls.COLS_LIST = map(list, zip(*new_question_list))

    @staticmethod
    def get_sudoku_type():
        return "cols"


class SudokuBox:
    BOX_LIST = []

    def __init__(self):
        pass

    @classmethod
    def set_data(cls, new_question_list):
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
        cls.BOX_LIST = all_box

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

    @staticmethod
    def print_sudoku(sudoku):
        print "\n\n\n"
        for val in sudoku:
            print val
        print "\n\n\n"

    @staticmethod
    def get_have_all_lines_been_filled(type_obj):
        print type_obj.unfilled_entries_list
        return all(type_obj.unfilled_entries_list)

    @staticmethod
    def initialize_sudoku_cell_obj(question_list_copy):
        sudoku_obj_list_list = list()

        for row_index, row in enumerate(question_list_copy):
            sudoku_row_list = list()
            for col_index, cell_value in enumerate(row):
                sudoku_cell_obj = SudokuCell(cell_value, row_index, col_index)
                sudoku_row_list.append(sudoku_cell_obj)
            sudoku_obj_list_list.append(sudoku_row_list)
        return sudoku_obj_list_list

    def set_value_if_can_be_identified(self, sudoku_obj):
        if sudoku_obj.value:
            print str(sudoku_obj.value) + " has already been set"
            return False

        sudoku_obj.possible_values_in_cell = sudoku_obj.possible_row_values & sudoku_obj.possible_box_values & sudoku_obj.possible_col_values

        if len(sudoku_obj.possible_row_values) == 1:
            sudoku_obj.value = list(sudoku_obj.possible_row_values)[0]
            self.update_missing_value_in_all_types(sudoku_obj)
            return True

        if len(sudoku_obj.possible_col_values) == 1:
            sudoku_obj.value = list(sudoku_obj.possible_col_values)[0]
            self.update_missing_value_in_all_types(sudoku_obj)
            return True

        if len(sudoku_obj.possible_box_values) == 1:
            sudoku_obj.value = list(sudoku_obj.possible_box_values)[0]
            self.update_missing_value_in_all_types(sudoku_obj)
            return True

        if len(sudoku_obj.possible_values_in_cell) == 1:
            sudoku_obj.value = list(sudoku_obj.possible_values_in_cell)[0]
            self.update_missing_value_in_all_types(sudoku_obj)
            return True

    @staticmethod
    def update_missing_value_in_all_types(sudoku_obj):
        SudokuRows.ROWS_LIST[sudoku_obj.rows_row_index][sudoku_obj.rows_col_index] = sudoku_obj.value
        SudokuColumns.COLS_LIST[sudoku_obj.cols_row_index][sudoku_obj.cols_col_index] = sudoku_obj.value
        SudokuBox.BOX_LIST[sudoku_obj.box_row_index][sudoku_obj.box_col_index] = sudoku_obj.value

    def result(self, sudoku_obj_list_list):
        for sudoku_ob_list in sudoku_obj_list_list:
            answer_row_list = list()
            for cell_obj in sudoku_ob_list:
                answer_row_list.append(cell_obj.value)
            self.answer_list.append(answer_row_list)

    def start(self):
        print "Process Begins"
        question_list = self.get_question_list()
        question_list_copy = deepcopy(question_list)

        self.print_sudoku(question_list_copy)

        # Set logical structures/rules present in a sudoku
        SudokuRows.set_data(question_list)
        SudokuColumns.set_data(question_list)
        SudokuBox.set_data(question_list)

        sudoku_obj_list_list = self.initialize_sudoku_cell_obj(question_list_copy)

        while True:
            is_value_set_this_iteration = False
            for sudoku_obj_list in sudoku_obj_list_list:
                for sudoku_cell_obj in sudoku_obj_list:
                    is_value_set = self.set_value_if_can_be_identified(sudoku_cell_obj)
                    if is_value_set:
                        # a value was successfully set
                        is_value_set_this_iteration = True

            if not is_value_set_this_iteration:
                break

        self.result(sudoku_obj_list_list)
        self.print_sudoku(self.answer_list)

        return


def main():
    sudoku_obj = SudokuSolver()
    sudoku_obj.start()


if __name__ == "__main__":
    main()
