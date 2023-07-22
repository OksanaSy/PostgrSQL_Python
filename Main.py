from Character import Character
from DBConnection import DBconnection

hp = Character("Harry", "Potter", "Human", "Wizard")
cn = Character("Conan", "Barbarian", "Human", "Warrior")
data = [hp, cn]

db = DBconnection("DnDParty")
cursor = db.get_db_cursor()
db.create_table()
db.delete_all()
db.insert_into_table(data)
print("List of all:")
for ch in db.select_all_from_table():
    print(ch.to_string())


db.insert_into_table(Character("Thorin", "Oakenshield", "Dwarf", "Warrior"))
print("\nList with added new character:")
for ch in db.select_all_from_table():
    print(ch.to_string())


print("\nList of all characters with class warrior")
for ch in db.select_where_from_table("cclas","Warrior"):
    print(ch.to_string())

print("\nList of all characters with id=1")
for ch in db.select_where_from_table("cid",1):
    print(ch.to_string())

db.update_class("Paladin",'cclas',"Warrior")
print("\nList of all characters with updated class")
for ch in db.select_where_from_table("cclas","Paladin"):
    print(ch.to_string())


db.delete_char('cname','Harry')
print("\nList of characters after delete:")
for ch in db.select_all_from_table():
    print(ch.to_string())


db.close_connection()
