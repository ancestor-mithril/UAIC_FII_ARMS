import csv

with open('gephi_anime_nodes.csv', mode='r') as csv_file_in:
    csv_reader = csv.reader(csv_file_in, delimiter=',')
    top = next(csv_reader)

    with open('filtered_nodes.csv', mode='w+') as csv_file_out:
        csv_writer = csv.writer(csv_file_out, delimiter=',')
        csv_writer.writerow(["ID", "Label", "Interval"])

        for row in csv_reader:
            if len(row) > 0:
                csv_writer.writerow([row[0], row[1], int(float(row[2]) ** 10)/(10**8)])
