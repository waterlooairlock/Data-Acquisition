import sys
sys.path.insert(0, 'interface')
import db

db.add_temp_reading(1, 1.5)
db.add_temp_reading(2, 1.5)
db.add_temp_reading(1, 2.5)
db.add_temp_reading(2, 2.5)

print(db.get_latest_temp_readings())