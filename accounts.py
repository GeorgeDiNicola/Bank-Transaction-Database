#!/usr/bin/env python3
#
# Author: George DiNicola
# Date Created: 12/12/2017
# Date Last Modified: 03/07/2019
# Python version 3.7
#
# The purpose of this program is to serve as a command-line utiliy database of bank accounts.
#
#
# Notes:
# Options for Argument 1:
#     -i : Displays account information
#     -h : Displays account history
#     -t : Allows the user to enter a transaction

import sys
import os
import math
import datetime

#-------------------------------------- Functions -----------------------------------------------------------------------------------------------

def get_account_balance(accounts, account_number):
    """for calculating an account balance
       @param accounts takes a dictionary of accounts
       @param account_number takes the 4-digit account number's balance to be calculated
       returns the current account balance
    """    
    acct_balance = 0
    for transaction in accounts[account_number]:
        if (transaction[2] == 'D'):
            acct_balance += float(transaction[3])
        else:
            acct_balance -= float(transaction[3])
    return acct_balance


def get_full_type(type_trans):
    """return deposit for d and withdrawal for w
       @param type_trans takes the type of transaction
    """
    if (type_trans == 'W'):
      return "Withdrawal"
    else:
      return "Deposit"


def check_valid(the_input, length):
    """check if input is valid for q or n (number does not exceed number of accounts)
       @param the_input takes the user input
       @param length takes the length of the dictionary
    """
    if (int(the_input) <= length):
        return True
    else:
        return False


def is_new_valid(new_acct_number, accounts):
    """check if the account number is new
       @param new_acct_number takes the account number
       @param accounts takes the dictionary of accounts
    """
    if (new_acct_number in accounts):
        return False
    else:
        return True


def valid_type(type_input):
    """check if type of transaction is valid
       @param type_inputtakes the type of the transaction
    """
    if (type_input == 'D' or type_input == 'W'):
        return True
    else:
        return False


def valid_acct_number(acct_input):
    """Check to see if the account number is valid (i.e. 4 digits long)
       @param acct_input takes the account number
    """
    length = len(acct_input)
    if (length == 4):
        return True
    else:
        return False


def check_quit(choice, accounts):
    """The check_quit function checks to see if the user has typed q to quit. It also writes out the log file.
         Starts by writing to a temporary file as an atomic operation
       @param choice takes the choice the user for quitting or continuing
    """
    if (choice == 'q' or choice == 'Q'):
        try:
            #write out to a new log file
            temp_file = open("temp_file", "w")

            data_list = []
            #create a list of new tuples to represent all pieces of data
            for key in accounts:
                for tup in accounts[key]:
                    temp_tuple = (key, tup[0], tup[1] , tup[2], tup[3])
                    data_list.append(temp_tuple)

            for tup in sorted(data_list, key = lambda x: x[2]):
                temp_file.write(tup[0] + ":" + tup[1] + ":" + tup[2] + ":" + tup[3] + ":" + tup[4] + "\n")
                temp_file.close()
        except:
            print("Error in writing out new database. Old database has been restored")
        else:
            #if temp_file successful, rename the log file
            os.rename("temp_file", os.environ["ACCT_LIST"])
            sys.exit()


def check_new(choice):
    """The check_new function determines if the user chooses to enter a transaction to a new account.
    """
    if (choice == 'n' or choice == 'N'):
        return True
    else:
        return False


def account_information(accounts):
    """Functon for displaying account info 
        @param accounts takes a dictionary
        Function does not return anything. Meant as an accessor for the user.
    """
    sorted_key_list = []
    #create an indexed list of keys in order of name on account
    for key in sorted(accounts, key=accounts.get):
        sorted_key_list.append(key)
    number_of_accounts = len(sorted_key_list)
    choice = " "
    while (choice != 'q'):   #will not! break is there a point?
        i = 1
        print("Info")
        print("----")
        #create an indexed list of sorted name/key pairs so numbers correspond to something
        for key in sorted_key_list:
            print(str(i) + ") " + accounts[key][0][0] + " " + key)
            i = i + 1
        print("q)uit")
        choice = input("Enter choice => ")
        check_quit(choice, accounts)
        validity = check_valid(choice, number_of_accounts)
        while (validity == False):
            print("Choice does not exist. Please choose a valid one from the list")
            choice = input("Enter choice => ")
            check_quit(choice, accounts)
            validity = check_valid(choice, number_of_accounts)
        choice = int(choice) - 1
        acct_chosen = sorted_key_list[choice]
        print("     account #:  " + str(acct_chosen))
        print("          name:  " + accounts[acct_chosen][0][0])
        print("       balance:  $" + str(format(get_account_balance(accounts, acct_chosen), '.2f')))
        choice = input("Would you like to return to the list of account holders? (y)es or (q)uit  ")
        check_quit(choice, accounts)
 

def history(accounts):
    """Access account history
       @param accounts takes a dictionary
       Function does not return anything. Meant as an accessor for the user.
    """
    #create an indexed list of keys in order of name on account
    sorted_key_list = []
    for key in sorted(accounts, key=accounts.get):
        sorted_key_list.append(key)
    number_of_accounts = len(sorted_key_list)
    choice = " "
    while (choice != 'q'):   #will not! break is there a point?
        i = 1
        print("History")
        print("-------")
        #create an indexed list of sorted name/key pairs so numbers correspond to something
        for key in sorted_key_list:
            print(str(i) + ") " + accounts[key][0][0] + " " + key)
            i = i + 1
        print("q)uit")
        choice = input("Enter choice => ")
        check_quit(choice, accounts)
        validity = check_valid(choice, number_of_accounts)
        while (validity == False):
            print("choice does not exist. Please choose a valid one from the list")
            choice = input("Enter choice => ")
            check_quit(choice, accounts)
            validity = check_valid(choice, number_of_accounts)
        choice = int(choice) - 1
        acct_chosen = sorted_key_list[choice]
        #extract the tuples from the dictionary using the choice
        list_of_transactions = accounts[acct_chosen]
        sorted_transactions = sorted(list_of_transactions, key = lambda x: x[1])
        for transaction in sorted_transactions:
            print("     " + transaction[1] + " " + get_full_type(transaction[2]) + " " + "$" + transaction[3])

def add_transaction(accounts):
    """Perform a transaction
       @param accounts takes a dictionary
       return the updated dictionary
    """
    choice = " "
    while (choice != 'q'):
        sorted_key_list = []
        #create an indexed list of keys in order of name on account
        for key in sorted(accounts, key=accounts.get):
            sorted_key_list.append(key)
        number_of_accounts = len(sorted_key_list)
        i = 1
        print("Add Transaction")
        print("---------------")
        #create an indexed list of sorted name/key pairs so numbers correspond to something
        for key in sorted_key_list:
            print(str(i) + ") " + accounts[key][0][0] + " " + key)
            i = i + 1
        print("n)ew account")
        print("q)uit")
        choice = input("Enter choice => ")
        check_quit(choice, accounts)
        new = check_new(choice)
        if (new == True):
            new_acct_number = input("Enter a new 4-digit account number  ")
            valid_new = is_new_valid(new_acct_number, accounts)
            length_validity = valid_acct_number(new_acct_number)
            while (valid_new == False or length_validity == False):
                new_acct_number = input("This account already exists or it is an invalid length. Please enter a new 4-digit account number  ")
                valid_new = is_new_valid(new_acct_number, accounts)
                length_validity = valid_acct_number(new_acct_number)
            accounts[new_acct_number] = []
            name = input("Please enter a name for the account holder  ")
            t_type = input("Enter the type of transaction (W - withdrawal, D - deposit)  ")
            t_type.upper()  #safeguard against user entering a lower case
            t_type = t_type.upper()
            t_valid = valid_type(t_type)
            while (t_valid == False):
                t_type = input("Invalid transaction type. Please enter a W for withdrawal or D for deposit  ")
                t_type = t_type.upper()
                t_valid = valid_type(t_type)
            amount = input("Please enter the amount (without the dollar sign!)  ")
            date = str(datetime.date.today())
            date = date[2:]
            #create transaction
            trans = (name, date, t_type, amount)
            accounts[new_acct_number].append(trans)
        else:
            validity = check_valid(choice, number_of_accounts)
            while (validity == False):
                print("choice does not exist. Please choose a valid one from the list")
                choice = input("Enter choice => ")
                check_quit(choice, accounts)
                validity = check_valid(choice, number_of_accounts)
            choice = int(choice) - 1
            acct_chosen = sorted_key_list[choice]
            t_type = input("Enter the type of transaction (W - withdrawal, D - deposit)  ")
            t_type = t_type.upper()  #safeguard against user entering a lower case
            t_valid = valid_type(t_type)
            while (t_valid == False):
                t_type = input("Invalid transaction type. Please enter a W for withdrawal or D for deposit  ")
                t_type = t_type.upper()
                t_valid = valid_type(t_type)
            amount = input("Please enter the amount (without the dollar sign!)  ")
            date = str(datetime.date.today())
            date = date[2:]
            name = accounts[acct_chosen][0][0]
            #create transaction
            trans = (name, date, t_type, amount)
            accounts[acct_chosen].append(trans)
    return accounts

#-------------------------------------------------------------------------------------------------------------------------------------------------

def main(argv):
   #initializatins
   accounts = {}
   acct_numbers = []

   #get file of account information and read it into my dictionary
   #filename = os.environ["ACCT_LIST"]
   filename = '/Users/georgedinicola/Desktop/untitled/ACCT_LIST.txt'
   accounts_file = open(filename, "r")
   line = accounts_file.readline()
   while line:
      #convert line into an array separated by colons.
      line = line.strip( '\t\n' )
      line_array = line.split(":")
      account_key = line_array[0]
      transaction = (line_array[1], line_array[2], line_array[3], line_array[4])
      #need to check if key already exists
      if (account_key in acct_numbers):
         accounts[account_key].append(transaction)
      else:
         accounts[account_key] = [transaction]
         acct_numbers.append(account_key)
      line = accounts_file.readline()

   #done with input file, close it
   accounts_file.close()

   if (len(sys.argv) < 2):
      print("\nNo options supplied. Please supply -i, -h, or -t after entering the accounts utility.")
      print("For more information about the options, enter the accounts utility with the -? option.\n")
      sys.exit()
   input_status = sys.argv[1]
   if (input_status == "-i"):
      account_information(accounts)
   elif (input_status == "-h"):
      history(accounts)
   elif (input_status == "-t"):
      accounts = add_transaction(accounts)   #because we are updating the account
   elif (input_status == "-?"):
      print("\nThe accounts program shows account information, account history, or can allow you to add a transaction to an account or new account.")
      print("To view account information, enter the accounts utility with the '-i' option. Then choose an account with the corresponding number to the left of it.")
      print("To view account history, enter the accounts utility with the the '-h' option. Then choose an account with the corresponding number to the left of it.")
      print("To add a transaction, enter the accounts utility with the '-t' option. Then choose an account to add a transaction to, or choose a new one by typing 'n'.\n")
   else:
      print("Invalid argument. Please enter a valid choice (-i,-h,-t, or -?)\n")

if __name__ == '__main__':
   main(sys.argv)











