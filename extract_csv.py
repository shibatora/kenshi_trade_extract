import struct
import csv

def get_data(filename):
	"""Reads binary data from the given file."""
	with open(filename, 'rb') as f:
		return f.read()

def get_trade_markups(data, city, item_dict):
	"""Extracts trade markup data for the given city from the binary data."""
	city_index = data.find(city.encode('utf-8'))
	if city_index == -1:
		print(f"City {city} not found in data.")
		return None
	
	trade_goods_index = data.find(b'trade goods', city_index)
	if trade_goods_index == -1:
		print(f"No trade goods data found for {city}.")
		return None
	
	# Extract the length of the array (4 bytes after "trade goods")
	array_length_offset = trade_goods_index + len(b'trade goods')
	array_length = struct.unpack_from('<I', data, array_length_offset)[0]
	
	entries = {}
	offset = array_length_offset + 4  # Move past array length
	
	for _ in range(array_length):
		# Read the string_id length (4 bytes)
		string_id_length = struct.unpack_from('<I', data, offset)[0]
		offset += 4
		
		# Read the string_id
		string_id = data[offset:offset + string_id_length].decode('utf-8')
		offset += string_id_length
		
		# Read the price markup (4 bytes)
		markup = struct.unpack_from('<I', data, offset)[0]
		offset += 4
		
		# Skip 8 bytes of padding
		offset += 8
		
		item_name = item_dict.get(string_id, "Unknown Item")
		
		item = {}
		item["string_id"] = string_id
		item["markup"] = markup

		entries[item_name] = item
		
		# entries.append({"string_id": string_id, "item_name": item_name, "markup": markup})
	
	return entries

def main():
	cities = [
		"The Hub",
		"Squin",
		"Admag",
		"Stack",
		"Bad Teeth",
		"Blister Hill",
		"Mongrel"
	]
	
	filename = "quick.save"
	
	item_dict = {
		"1534063-Newwworld.mod": "Simple Rug",
		"97903-rebirth.mod": "Authentic Skeleton Repair Kit",
		"97089-rebirth.mod": "Crossbow Parts",
		"97090-rebirth.mod": "Spring Steel",
		"1914-gamedata.base": "Water",
		"50517-Newwworld.mod": "Thinfish",
		"42322-changes_otto.mod": "The Holy Flame",
		"1932-gamedata.base": "Strawflour",
		"1435-gamedata.base": "Splint Kit",
		"43404-changes_otto.mod": "Tools",
		"42320-changes_otto.mod": "Small Emperor Statue",
		"45557-changes_otto.mod": "Skeleton Eye",
		"42243-rebirth.mod": "Raw Meat",
		"1866-gamedata.base": "Raw Iron",
		"43397-changes_otto.mod": "Motor",
		"43960-rebirth.mod": "Meatwrap",
		"5348-gamedata.base": "Lantern",
		"42159-gamedata.base": "Iron Plates",
		"43862-changes_otto.mod": "Wrench",
		"42309-changes_otto.mod": "Greenfruit",
		"1913-gamedata.base": "Wheatstraw",
		"42189-rebirth.mod": "Generator Core",
		"42307-changes_otto.mod": "Riceweed",
		"1514-gamedata.base": "Fuel",
		"18020-gamedata.base": "Skeleton Repair Kit",
		"43396-changes_otto.mod": "Hinge",
		"43959-rebirth.mod": "Foodcube",
		"42164-gamedata.base": "Electrical Components",
		"42334-changes_otto.mod": "Dried Meat",
		"50568-rebirth.mod": "Dried Gristle Flaps",
		"50518-Newwworld.mod": "Dried Fish",
		"43395-changes_otto.mod": "Skeleton Muscle",
		"42178-rebirth.mod": "Cotton",
		"42160-gamedata.base": "Copper Alloy Plates",
		"43398-changes_otto.mod": "Power Core",
		"42304-changes_otto.mod": "Cactus",
		"16855-nodes_otto1.mod": "Book",
		"1965-gamedata.base": "Hemp",
		"43316-rebirth.mod": "Bloodrum",
		"43955-rebirth.mod": "Cooked Vegetables",
		"43393-changes_otto.mod": "Capacitor",
		"43961-rebirth.mod": "Dustwich",
		"42241-rebirth.mod": "Animal Skin",
		"42310-changes_otto.mod": "Sake",
		"42313-changes_otto.mod": "Animal Claw",
		"2288-gamedata.base": "Armour Plating",
		"43956-rebirth.mod": "Chewsticks",
		"1946-gamedata.base": "Bread",
		"1230-gamedata.base": "Hashish",
		"43399-changes_otto.mod": "Press",
		"1015-gamedata.base": "Cactus Rum",
		"1359-gamedata.base": "Advanced First Aid Kit",
		"50514-Newwworld.mod": "Grand Fish",
		"42337-changes_otto.mod": "Ration Pack",
		"42158-gamedata.base": "Copper",
		"1436-gamedata.base": "Advanced Splint Kit",
		"42311-changes_otto.mod": "Grog",
		"42315-changes_otto.mod": "Animal Teeth",
		"580-gamedata.base": "Building Material",
		"579-gamedata.base": "Steel Bars",
		"43394-changes_otto.": "CPU Unit",
		"585-gamedata.": "Luxury Goods",
		"1515-gamedata.base": "Raw Stone",
		"584-gamedata.base": "Fabrics",
		"2289-gamedata.base": "Chainmail Sheets",
		"515-gamedata.base": "Standard Fist Aid Kit",
		"43957-rebirth.mod": "Gohan",
		"583-gamedata.base": "Robotics Components",
		"1016-gamedata.base": "Rice Bowl",
		"42314-changes_otto.mod": "Animal Horn",
		"582-gamedata.base": "Medical Supplies",
		"581-gamedata.base": "Hacksaw",
		"2292-gamedata.base": "Leather",
		"209-gamedata.base": "Basic First Aid Kit",
		"42318-changes_otto.mod": "Gears"
	}
	
	data = get_data(filename)
	result = []
	
	for city in cities:
		markups = get_trade_markups(data, city, item_dict)
		if markups:
			for item_name, info in markups.items():
				result.append({
					"city": city,
					"item_name": item_name,
					"string_id": info["string_id"],
					"markup": info["markup"]
				})
	
	# Write to CSV
	with open("extracted_data.csv", "w", newline='', encoding="utf-8") as csvfile:
		fieldnames = ["city", "item_name", "string_id", "markup"]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		
		writer.writeheader()
		for row in result:
			writer.writerow(row)
	
	print("Trade markups have been saved to extracted_data.csv")

if __name__ == "__main__":
	main()
