#Program to process input sale comments as strings
#record every sale and process every message
#@Author: Sahiti Penna


import sys
import time

sale_count = 0
count = 0
sale_element_count = 0
total_element_value = 0
sale_dict = {}
adjustment_record = {}
record=""

f=open('log.txt', 'w+')

def log_adjustments():
    f = open('log.txt', 'a+')
    f.write("50 messages received. \n"
          "Recording adjustments \n"
          "Pausing application \n")
    f.write("adjustment record is: %s\n "
    %adjustment_record)
    time.sleep(2)
    f.close()


def log_sales():
    f = open('log.txt', 'a+')
    #log a report detailing the number of sales of each product and their total value.
    for key,value in sale_dict.items():
        f.write("Total count sold: " + key + "=> " + " Total Value"+ str(value) +"\n")
    #do something
    f.close()

def do_adjustments(adj_type, adj_value, total_count, total_value):
    if adj_type == 'add':
        print("add")
        total_value = int(total_value) + total_count * adj_value
    if adj_type == 'subtract':
        print("sub")
        total_value = total_value - (adj_value * total_count)
    if adj_type == 'multiply':
        total_value = total_value * total_count * adj_value
    return total_value

for line in sys.stdin:
    print(line)
    sale_message = line
    if sale_message == "\n":
        print("Unexpected sale message format- Empty message")
        continue
    sale_elements = sale_message.strip().split(" ")  # obtaining words

    #message type 2
    if "sales" in sale_message:
        #Message type 2
        if len(sale_elements) != 6:
            print("Unexpected sale message format")
            continue
        try:
            sale_type = sale_elements[3]
            if not sale_type in sale_dict:
                print("case 1")
                # value is [sale_element_count,total_price]
                sale_dict[sale_elements[3]] = [int(sale_elements[0]), int(sale_elements[5])]
                print(sale_dict)
            else:
                print("case 2")
                print(sale_type)
                total_element_value = sale_dict[sale_type][1]
                sale_element_count = sale_dict[sale_type][0]
                print(sale_dict.values())
                sale_element_count += int(sale_elements[0])
                total_element_value += int(sale_elements[0])*int(sale_elements[5])
                sale_dict[sale_type] = [sale_element_count, total_element_value]
                print(sale_dict)
            count+=1
            print(count)
        except ValueError:
            print("Unexpected message value format")
            continue

    #message type 3: add 20 apples

    if any(x in sale_elements for x in ['add', 'subtract', 'multiply']):
        if len(sale_elements) != 3:
            print("Unexpected sale message format")
            continue
        try:
            sale_type = sale_elements[2]
            if sale_type in sale_dict:
                sale_element_count = sale_dict[sale_type][0]
                total_element_value = sale_dict[sale_type][1]
                total_element_value = do_adjustments(sale_elements[0],int(sale_elements[1]),
                                                 sale_element_count, total_element_value)
                sale_dict[sale_type] = [sale_element_count, total_element_value]
                #record adjustment
                record = sale_elements[0]+" "+sale_elements[1]
                adjustment_record.setdefault(sale_type, []).append(record)
                print(sale_dict)
            else:
                sale_dict[sale_type]= [1, sale_elements[1]]
                record = sale_elements[0]+" "+sale_elements[1]
                adjustment_record.setdefault(sale_type, []).append(record)
            count += 1
        except ValueError:
            print("Unexpected message value format")
            continue

    #message type 1- apple at 10
    else:
        if len(sale_elements) !=3:
            print("Unexpected message value format")
            continue
        try:
            sale_type = sale_elements[0]
            sale_count = sale_count + 1
            if not sale_type in sale_dict:
                sale_dict[sale_type] = [1,int(sale_elements[2])]
                print(sale_dict)
                count += 1
            else:
                total_element_value = sale_dict[sale_type][1]
                sale_element_count = sale_dict[sale_type][0]
                sale_element_count += 1
                total_element_value = total_element_value + int(sale_elements[2])
                sale_dict[sale_type] = [sale_element_count, total_element_value]
                print(sale_dict)
                count += 1
        except ValueError:
            print("Unexpected message format")
            continue
    if count == 10:
        #log a report with the number of sales of each product and their total value.
        log_sales()
    if count == 50:
        # log that it is pausing, stop accepting new messages and log a report of the
        # adjustments that have been made to each sale type while the application was running.
        count =0
        print("recording")
        log_adjustments()



