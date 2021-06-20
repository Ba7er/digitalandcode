import csv
import os


def handle_uploaded_file(file):
    # @TODO rename the file after it is updasted
    # @TODO in case of huge file size, we should use streaming instead of uploading the whole file in memory
    with open('t.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',',
                                skipinitialspace=True)
        teachersList = []
        row_count = 0
        for row in csv_reader:
            if(row_count != 0):  # skip first iterator
                subjects_list = row[6].split(',')
                teacherDict = {'first_name': row[0], 'last_name': row[1], 'email': row[3],
                               'phone_number': row[4], 'room_number': row[5], 'subjects': subjects_list, }
                teachersList.append(teacherDict)

            else:
                row_count += 1
        os.remove('t.csv')
        return teachersList
