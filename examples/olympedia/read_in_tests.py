import requests, sys, time, re, csv, ast, joblib

with open('tuple_list.txt','r') as f:
   my_set = ast.literal_eval(f.read())

print(my_set, "\ntype: ", type(my_set))

print("my_set[1][1]: ", my_set[1][1])