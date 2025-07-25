# Kenshi Trade Extract Scripts

## Disclaimer

I wrote this script very quickly for my own trader playthrough. I didn't use any mods so it may or may not work with mods. There's no harm in trying, but there's no guarantee it will work and I won't fix it in case it doesn't. You're on your own.

## Requirements:

Python 3.6+

## How to Use:

1. Download either or all python files.
2. Move the script into one of your Kenshi save directories. You got the right directory if there is a file called "quick.save" in there.
3. Open the script with a text editor of your choice. Scroll down until you find the following text passage:

![Cities code section](/cities.jpg)

4. Add or remove any cities you're interested in.
5. (Optional) If you have any mods installed that add trade goods, you will need to open the mod in the construction set that comes with Kenshi and find the ID associated with that item. Then add that ID with the corresponding name to the item_dict below in the script. It should work with mods, but I haven't tested it. So no guarantees.
6. Save the file.
7. Open a terminal of your choice and run the script with Python.

If everything worked it should output either `extracted_data.json` or `extracted_data.csv`.
