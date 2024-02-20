import csv

input_file = "Data/00effd348b9c800790820fce60d86d4d56534be2ca3371f75da7e1d741c8caac.csv"
output_file = "Data/consumption.csv"
line_count = 0

with open(input_file, 'r') as file_in, open(output_file, 'w', newline='') as file_out:
    reader = csv.reader(file_in)
    writer = csv.writer(file_out)
    
    for row in reader:
        line_count += 1
        
        if line_count % 950 == 0:
            writer.writerow(row)
