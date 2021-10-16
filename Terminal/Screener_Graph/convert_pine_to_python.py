#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 19:21:33 2021

@author: abhishek
"""
import re

# misc
def comment(line):
    _ = False
    if re.findall("strategy|study|//", line):
        line = line.split(' ')
        line.insert(0, '#')
        line = ' '.join(line)
        _ = True
    return line, _

# logic >>>> add more logic support
def logic(line):
    if re.findall("if ", line):
        line = line.split(' ')
        line[-1] = line[-1].strip('\n')
        line.append(':\n')
        line = ' '.join(line)
    return line

# booleans
def boolean(line):
    boolx = re.findall("true|false", line)
    for booly in boolx:
        string = line.split(booly)
        booly = booly.replace(" ", "").capitalize()
        string.insert(-1, booly)
        line = ''.join(string)
    return line

# operators
def operator(line):
    op = re.findall("\?|:=", line)
    op.append(' ')
    if op[0] == ':=':
        string = line.split(op[0])
        op[0] = '='
        string.insert(-1, op[0])
        line = ''.join(string)

    if op[0] == '?':
        try:
            s1 = line.split("=")
            string = s1[-1].replace(" ", "")
            string = string.split(op[0])
            condition = string[0].replace(" ", "")
            sub = string[1].replace(" ", "")
            sub = sub.split(":")
            val1 = str(sub[0])
            val2 = str(sub[1])
            var = s1[0].replace(" ", "")
            if var and condition and val1 and val2:
                string = '{0} = lambda {1}, {2}, {3}: {2} if {1} else {3}'.format(var, condition, val1, val2)
            else:
                string = 'failed to interpret line, make sure it is formatted as:\na = b ? c : d'
            line = string
        except Exception as e:
            line = 'failed to interpret line, make sure it is formatted as:  na = b ? c : d'
    return line

# builtins >>>>> add more builtin function support 
def builtins(line):
    funcx = re.findall("input\(|alertcondition\(", line)
    funcx.append(' ')
    if funcx != [' ']:
        funcy = funcx[0]
        if funcy == 'alertcondition(':
            string = line.split(funcy)
            funcy = funcy.replace("alertcondition(", "alertcondition(")
            string.insert(-1, funcy)
            line = ''.join(string)
        if funcy == 'input(':
            string = line.split(funcy)
            funcy = funcy.replace("input(", "Input(")
            string.insert(-1, funcy)
            line = ''.join(string)
    return line

# =============================================================================
# 
# def Equal(line):
#     funcx = re.findall('[^.][^.] = [^.] == [^.]',line)
#     funcx.append(' ')
#     if funcx != [' ']:
#         funcy = funcx[0].strip()
#         x = funcy[-1]
#         y = funcy.split('==')[0].strip()
#         
# =============================================================================
# functions
def functions(line):
    funcx = re.findall("=>", line)
    if funcx:
        line = line.split(funcx[0])
        n1 = line[0].replace(" ", "")
        n2 = line[1].replace(" ", "")
        if '\t' not in n2:
            string = 'def {0}:\n\t{1}'.format(n1, n2)
        else:
            string = 'def {0}:\n{1}'.format(n1, n2)
        line = string
    return line

def Hash(line):
    hex_value = re.findall("#[^.][^.][^.][^.][^.][^.]", line)
    if len(hex_value)>0:
        line = line.replace(hex_value[0],"color")
    return line



def Convert(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        filename = file.split(".")[0]
    filename = 'python_script.py'
    with open(f'./tempDir/{filename}', 'w') as f:  
        f.write('from functions import *\n\n')
        f.write('import numpy as np\n\n')
        f.write('def Find_signals(Data,Symbol):\n\n')
        f.write('\tclose=Data.Close\n\n')
        f.write('\thigh=Data.High\n\n')
        f.write('\tlow=Data.Low\n\n')
        f.write('\topen=Data.Open\n\n')
        f.write('\tprint(Symbol,":")\n\n')
        count = 0 
        for line in lines:
            line, c = comment(line)
            if not c:
                line = functions(logic(boolean(operator(functions(line)))))
            line = builtins(line)
            #line = line.replace('color=','')
            line = line.replace('.','_')
            #line = line.replace('color =','')
            if count > 5:
                line = Hash(line)
            print(line)
            count+=1
            f.write('\t'+line)
        f.write("\n\tfig,axs=mpf.plot(Data,addplot=indicator,tight_layout=True,returnfig=True)")
        f.write("\n\tplt.show()")
        f.write("\n\treturn 'Done'")
        f.write("\nFind_signals.Indicator = []")
        
        
        
        