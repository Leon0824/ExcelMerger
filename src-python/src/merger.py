from sys import argv, exit
from pathlib import Path
from glob import glob
from collections import OrderedDict
import tempfile

import xlwings as xw

def merge_sheets(wb: xw.Book) -> None:
    sheets: list[xw.Sheet] = wb.sheets
    main_sheet: xw.Sheet = sheets[0]
    main_sheet_last_row: int = main_sheet.used_range.last_cell.row

    while len(sheets) > 1:
        second_sheet: xw.Sheet = sheets[1]
        second_sheet_last_row: int = second_sheet.used_range.last_cell.row
        second_sheet_last_column: int = second_sheet.used_range.last_cell.column
        second_sheet.range((2, 1), (second_sheet_last_row, second_sheet_last_column)).copy(destination=main_sheet.range((main_sheet_last_row + 1, 1)))
        second_sheet.delete()
        main_sheet_last_row: int = main_sheet.used_range.last_cell.row

def main() -> None:

    argvs: list[str] = argv[1:]
    extracted_argvs: list[str] = []

    # Check files quantity
    if not argvs: raise FileNotFoundError

    # Extract wildcard to path strings
    for path in argvs:
        p: Path = Path(path).absolute()
        if p.stem == '*':
            glob_paths: list[str] = glob(str(p))
            extracted_argvs.extend(iter(glob_paths))
        else:
            extracted_argvs.append(path)


    # Check files existence
    for path in extracted_argvs:
        if not Path(path).is_file() or not Path(path).exists(): raise FileNotFoundError

    # Convert to absolute path
    absolute_paths: list[Path] = [Path(path).resolve() for path in extracted_argvs]
    # absolute_paths: list[Path] = list(map(lambda path: Path(path).resolve(), extracted_argvs))

    # Deduplicate
    absolute_paths = list(OrderedDict.fromkeys(absolute_paths))

    main_file_path: Path = absolute_paths[0]

    # Check files suffix
    allowed_suffix: tuple[str] = ('.xlsx', '.xls')
    for path in absolute_paths:
        if path.suffix.lower() not in allowed_suffix: raise FileNotFoundError

    with xw.App(add_book=False, visible=False) as app:
        try:
            main_wb: xw.Book = app.books.open(main_file_path)
        except Exception as e:
            print(e)
            exit(1)
        main_wb_sheet: xw.Sheet = main_wb.sheets[0]

        if len(main_wb.sheets) > 1: merge_sheets(main_wb)

        if len(absolute_paths) > 1:
            for path in absolute_paths[1:]:
                second_wb: xw.Book = app.books.open(path)
                if len(second_wb.sheets) > 1: merge_sheets(second_wb)

                second_wb_sheet: xw.Sheet = second_wb.sheets[0]
                second_wb_sheet.copy(after=main_wb_sheet)

            merge_sheets(main_wb)

        main_wb_sheet.name = f'{main_wb_sheet.name}.merged'

        temp_path = Path(tempfile.gettempdir())
        new_file_path = temp_path.joinpath(f'{main_file_path.stem}.merged.xlsx')
        main_wb.save(new_file_path)
        print(new_file_path)
        # breakpoint()

if __name__ == '__main__':
    main()
