import csv
import re


def format_name(book_list):
    format_book = []
    for name in book_list:
        list_name = (name[0] + ' ' + name[1] + ' ' + name[2]).strip()
        list_name = list_name.split()
        name[0] = list_name[0]
        name[1] = list_name[1]
        if len(list_name) == 3:
            name[2] = list_name[2]
        format_book.append(name)
    return format_book


def format_str(book_list):
    list_name = []
    for name in book_list:
        list_name.append(name[0])
    list_index = list()
    for i in range(len(list_name)):
        for j in range(1, len(list_name)):
            if (list_name[i] == list_name[j]) and (i != j):
                for k in range(len(book_list[i])):
                    try:                # Добавил обработчик ошибок в связи с лишней запятой в 4 строке файла
                        if book_list[i][k] == book_list[j][k]:
                            continue
                        else:
                            if book_list[i][k] == '':
                                book_list[i][k] = book_list[j][k]
                    except IndexError:
                        book_list[i].remove(book_list[i][k])
                list_index.append(j)
    unique_list = list()
    for item in book_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def format_phone(book_phone):
    final_book = list()
    for item in book_phone:
        str_temp = "|".join(item)
        str_temp = re.sub(r"(\+7|8)\s*\(*(\d\d\d)\)*[\s-]*(\d\d\d)[\s-]*(\d\d)[\s-]*(\d\d)", r"+7(\2)\3-\4-\5",
                          str_temp)
        str_temp = re.sub(r"(\+7|8)\s*\(*(\d\d\d)\)*[\s-]*(\d\d\d)[\s-]*(\d\d)[\s-]*(\d\d)[\s-]*\(*(\w+\.*)\s*(\d+)\)*",
                          r"+7(\2)\3-\4-\5 \6\7", str_temp)
        final_book.append(re.split("\|", str_temp))
    return final_book


if __name__ == '__main__':
    with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    book = format_name(contacts_list)
    unique_book = format_str(book)
    book_for_file = format_phone(unique_book)

    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        data_writer = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        data_writer.writerows(book_for_file)
