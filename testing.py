# THIS FILE CONTAINS USAGE EXAMPLE AND TESTING

import os
from btreedb import DB_Agent

print('----> TESTING DELETING', end='\n\n')

print('#1 DELETE EXAMPLE', end='\n\n')

db = DB_Agent(2, file_caching=False)
for i in range(30):
    db.insert_pair(i, 100 - i)
print('FULL TREE [BEFORE DELETION]', end='\n\n')
db.print_tree()
print()

for i in range(30, -1, -1):
    db.delete_by_key(i)
print('EMPTY TREE [AFTER DELETION]', end='\n\n')
db.print_tree()
print(end='\n\n')

print('#2 DELETION ON AN EMPTY TREE', end='\n\n')

db = DB_Agent(2, file_caching=False)
print('[BEFORE DELETION]', end='\n\n')
db.print_tree()
print(end='\n\n')

print('[AFTER DELETION] (SHOULD NOT BE ANY EXCEPTIONS THROWN)', end='\n\n')
try:
    db.delete_by_key(1)
    print('<NO EXCEPTIONS>', end='\n\n')
except:
    print('<EXCEPTION>')
db.print_tree()
print(end='\n\n')

print('#3 DELETING ELEMENT BY NON-EXISTING KEY', end='\n\n')

db = DB_Agent(2, file_caching=False)
db.insert_pair(1, 1)
print('[BEFORE DELETION]', end='\n\n')
db.print_tree()
print()

print('[AFTER DELETION] (SHOULD NOT BE ANY EXCEPTIONS THROWN)', end='\n\n')
try:
    db.delete_by_key(2)
    print('<NO EXCEPTIONS>')
except:
    print('<EXCEPTION>')
db.print_tree()
print(end='\n\n')

###

print('----> TESTING INSERTION', end='\n\n')

print('#1 INSERT EXAMPLE', end='\n\n')

db = DB_Agent(2, file_caching=False)
print('[BEFORE INSERT]', end='\n\n')
db.print_tree()
print()

for i in range(10):
    db.insert_pair(i, 90 - i)
print('[AFTER INSERT]', end='\n\n')
db.print_tree()
print(end='\n\n')

print('#2 INSERT SAME KEY', end='\n\n')

db = DB_Agent(2, file_caching=False)
db.insert_pair(1, 1)
print('[BEFORE INSERT]', end='\n\n')
db.print_tree()
print()

print('[INSERT] (SHOULD THROW AN EXCEPTION)', end='\n\n')
try:
    db.insert_pair(1, 2)
    print('<NO EXCEPTION TO THROWN>', end='\n\n')
except:
    print('<EXCEPTION WAS THROWN>', end='\n\n')

print('[AFTER INSERT]', end='\n\n')
db.print_tree()
print(end='\n\n')

print('#3 TESTING KEY TYPING', end='\n\n')

db = DB_Agent(2, file_caching=False)
first_key, second_key = 1, '1'
print(f'[FIRST INSERT] (key type = {type(first_key)})', end='\n\n')
db.insert_pair(first_key, 100)
db.print_tree()
print()

print(f'[SECOND INSERT] (key type = {type(second_key)}) (SHOULD THROW AN EXCEPTION)', end='\n\n')
try:
    db.insert_pair(second_key, 100)
    print('<NO EXCEPTION TO THROWN>', end='\n\n')
except:
    print('<EXCEPTION WAS THROWN>', end='\n\n')
db.print_tree()
print()

###

print('----> TESTING SEARCHING', end='\n\n')

print('#1 SEARCHING EXAMPLE', end='\n\n')

db = DB_Agent(2, file_caching=False)
for i in range(21):
    db.insert_pair(i, 50 - i)
print('[INITIAL TREE]', end='\n\n')
db.print_tree()
print()

print('[SEARCHING INSERTED VALUES] (SHOULD NOT BE ANY EXCEPTIONS THROWN)', end='\n\n')
try:
    for i in range(20, -1, -1):
        assert db.find(i) == 50 - i, 'FOUND WRONG VALUE'

    print('<NO EXCEPTIONS>', end='\n\n')
except:
    print('<EXCEPTION>', end='\n\n')

print('#2 SEARCHING NON-EXISTING KEY', end='\n\n')

db = DB_Agent(2, file_caching=False)
db.insert_pair(1, 1)
print('[INITIAL TREE]', end='\n\n')
db.print_tree()
print()

print('[SEARCHING WRONG KEY] (SHOULD THROW AN EXCEPTION)', end='\n\n')
try:
    db.find(100)
    print('<NO EXCEPTIONS>', end='\n\n')
except:
    print('<EXCEPTION>', end='\n\n')

###

print('----> TESTING FILE-CACHING', end='\n\n')

print('#1 ENABLED FILE-CACHING', end='\n\n')

db = DB_Agent(2, file_caching=True)
for i in range(10):
    db.insert_pair(i, i)
print('[INITIAL TREE]', end='\n\n')
db.print_tree()
print()

db.save_data()
print('[CHECKING \'storage.txt\' EXISTENCE] (SHOULD THROW NO EXCEPTIONS)', end='\n\n')
try:
    assert os.path.exists('storage.txt'), 'NO CACHING FILE WAS CREATED'
    print('<NO EXCEPTIONS>', end='\n\n')
except:
    print('<EXCEPTION>', end='\n\n')

print('[CHECKING CORRECTNESS OF SERIALIZATION]', end='\n\n')
db2 = DB_Agent(2, file_caching=True)

print('<ORIGINAL TREE>')
db.print_tree()
print()
print('<RECREATED TREE>')
db2.print_tree()
print()
os.remove('storage.txt')

print('#2 DISABLED FILE-CACHING', end='\n\n')

db = DB_Agent(2, file_caching=False)
db.save_data()
print('[CHECKING \'storage.txt\' EXISTENCE] (SHOULD THROW NO EXCEPTIONS)', end='\n\n')
try:
    assert not os.path.exists('storage.txt'), 'FILE SHOULD NOT EXIST'
    print('<NO EXCEPTION>', end='\n\n')
except:
    print('<EXCEPTION>', end='\n\n')

###

external_tree = DB_Agent(2, file_caching=True)
for i in range(5):
    external_tree.insert_pair(i, i)
external_tree.save_data()

print('----> TESTING ABILITY TO PROVIDE DATA', end='\n\n')

print('#1 PROVIDING EXISTING FILE', end='\n\n')

db = DB_Agent(2, file_caching=False)
print('[PROVIDING EXISTING FILE] (\'storage.txt\' from another tree)', end='\n\n')
db.provide_data('storage.txt')

print('<EXTERNAL_TREE>')
external_tree.print_tree()
print()
print('<RECREATED_TREE>')
db.print_tree()
print()
os.remove('storage.txt')

print('#2 PROVIDING NON-EXISTING FILE', end='\n\n')

db = DB_Agent(2, file_caching=False)
print('[PROVIDING NON-EXISTING FILE] (SHOULD THROW AN EXCEPTION)', end='\n\n')
try:
    db.provide_data('NON-EXISTING FILE')
    print('<NO EXCEPTIONS>', end='\n\n')
except:
    print('<EXCEPTION>', end='\n\n')
