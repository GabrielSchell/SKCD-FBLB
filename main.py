# Made by Gabriel Schell, 10/2023, CC-BY-NB
# -------------------------------
# ENTERING THE IMPORT PART

from PIL import Image, ImageDraw, ImageFont
from pyfiglet import figlet_format
from colorama import Fore, Style
from os import path, makedirs
from pandas import read_csv
from json import dump, dumps, load
from argparse import ArgumentParser
from sys import exit
import numpy

# EXITING THE IMPORT PART
# -------------------------------
# ENTERING THE INTRO PART

text = "SKILL  CARDS FABLAB"
text = figlet_format(text)
print(text)
print("------")
print("\nThis script will generate a card for each member of the FabLab that has at least some knowledge.")
print("If there's any error, please do the following:")
print("- Check the labels variables in the code. The labels are the names of the columns in the spreadsheet and they are case sensitive.")
print("- If the labels are correct, check the spreadsheet's URL. It should be the one that ends with 'output=csv'")
print("- If the URL is correct, check if the spreadsheet is published to the web.\n\nTo do so in "+Fore.GREEN+"Google Sheet"+Style.RESET_ALL +", go to\n-> File \n-> Share\n-> Publish to the web... \n-> (select the correct tab and choose the CSV format) \n-> Publish\n")
print("------")

# EXITING THE INTRO PART
# -------------------------------
# ENTERING THE EXTERIOR VARIABLES DEFINITION PART

global parser
parser = ArgumentParser(
    description="",
    epilog="",
)

parser.add_argument("-ft", "--first_time", help="A beginner guide on how to use this script", action="store_true")
parser.add_argument("-v", "--var", help="See and modify variables", action="store_true")
parser.add_argument("-cn","--config_name", help="Choose the config file you want to use")
args = parser.parse_args()

if args.config_name == None: # If no config file is specified, the default one is used
    cfl=f"./default.json"
    print("No config file specified, using the default one\r")
    if path.isfile(cfl) and (path.getsize(cfl) != 0): # If the config file exist and is not empty, it is loaded
        EV = load(open(cfl)) #EXTERIOR VARIABLES
    elif path.isfile(cfl) and (path.getsize(cfl) == 0): # If the config file exist but is empty, it is filled with the default values
        def_config = {
            "url": ["https://docs.google.com/spreadsheets/d/e/LeTtErSAnDnUmBeRs/pub?gid=123456789&single=true&output=csv", "Spreadsheet (CSV) URL/path.\nFORMAT: {fullURL} or ./{subfolders}/{filename}.csv",],
            "LQPS": ["PQS", "Label for Qualifications Point Sum. The label of the column where the sum of the qualifications points is stored.\nFORMAT: {columnname}"],
            "picture_column": ["Photos", "column where the name of pictures of the members are stored.\nFORMAT: {columnname}"],
            "save_folder": ["cards", "folder where the cards will be saved.\nFORMAT: ./{pathtofolder}"],
            "picture_folder": ["photos", "folder where the pictures of the members are stored.\nFORMAT: ./{pathtofolder}"],
            "h_font_path": ["./Staatliches.ttf", "path to the font file for the heading. It needs to be a TrueTypeFont format (.ttf).\nFORMAT: ./{subfolders}/{filename}.ttf"],
            "t_font_path": ["./Gabarito.ttf", "path to the font file for the text. It needs to be a TrueTypeFont format (.ttf).\nFORMAT: ./{subfolders}/{filename}.ttf"],
            "g_diam_w": ["./temp2.png", "path to the white diamond image.\nFORMAT: ./{subfolders}/{filename}.{imageextension}"],
            "g_diam_b": ["./temp.png", "path to the black diamond image.\nFORMAT: ./{subfolders}/{filename}.{imageextension}"],
            "bg": ["./canvas.png","path to the background image.\nFORMAT: ./{subfolders}/{filename}.{imageextension}"],
            "h_width_fraction": [0.95, "portion of canvas width the HEADING text width aim to be.\nFORMAT: {number}"],
            "t_width_fraction": [1, "portion of canvas width the text width aim to be.\nFORMAT: {number}"],
            "dpi": [300, "dots per inch.\nFORMAT: {number}"],
            "canvasx": [10.5, "canvas width in cm.\nFORMAT: {number}"],
            "canvasy": [14.8, "canvas height in cm.\nFORMAT: {number}"],
            "XH": [375, "X coordinate of the heading.\nFORMAT: {number}"],
            "YH": [375, "Y coordinate of the heading.\nFORMAT: {number}"],
            "XK": [50, "X coordinate of the key.\nFORMAT: {number}"],
            "GYK1": [550, "Y coordinate1 of the key.\nFORMAT: {number}"],
            "GYK2": [85, "Y coordinate2 of the key.\nFORMAT: {number}"],
            "Px": [3.5, "Photo width in cm.\nFORMAT: {number}"],
            "Py": [4.5, "Photo height in cm.\nFORMAT: {number}"],
            "P_y": [200, "Y coordinate of the picture.\nFORMAT: {number}"],
            "redux1": [0.7, "reduction factor of the picture after a first resize to standart photo format.\nFORMAT: {number}"],
            "Dx": [0.5, "Diamond width in cm.\nFORMAT: {number}"],
            "Dy": [0.5, "Diamond height in cm.\nFORMAT: {number}"],
            "redux2": [1.2, "reduction factor of the picture after a first resize.\nFORMAT: {number}"]
        }
        with open(cfl, "w") as json_conf:
            dump(def_config, json_conf, indent=4)
        print(Fore.YELLOW + f"The config file '{cfl}' is ready. Please restart the script\r"+ Style.RESET_ALL)
        print("------\n")
        json_conf.close()
        exit(0)
    else:
        try : # If the config file doesn't exist, it is created
            open(cfl, 'x+').close()
            print(Fore.YELLOW + f"Config file '{cfl}' not found, creating one. Please restart the script\r"+ Style.RESET_ALL)
            print("------")
        except Exception as e:
            print(Fore.RED + f"\nCan't create a config file ({cfl}):\r({e})\n"+ Style.RESET_ALL)  
            print("------\n")
            raise ImportError
        finally:
            exit(0)
else: # If a config file is specified, it is used
    cfl=f"./{args.config_name}.json"
    print(f"Config file specified, using {cfl}")
    if path.isfile(cfl) and (path.getsize(cfl) != 0): # If the config file exist and is not empty, it is loaded
        EV = load(open(cfl)) #EXTERIOR VARIABLES
        print("Config file loaded\n------")
    elif path.isfile(cfl) and (path.getsize(cfl) == 0): # If the config file exist but is empty, user is invited to fill it
        print(Fore.YELLOW + f"The config file {cfl} is empty\r"+ Style.RESET_ALL)
        print(Fore.YELLOW + f"Please fill the config file with your values\r"+ Style.RESET_ALL)
        print(Fore.YELLOW + f"If your comfortable with command lines, you can use arguments (-h to know more)\r"+ Style.RESET_ALL)
        print(Fore.YELLOW + f"If your not, you can edit the file ({cfl})\n"+ Style.RESET_ALL)
        print("------")
        exit(0)
    else:
        try : # If the config file doesn't exist, it is created
            open(cfl, 'x+').close()
            print(Fore.YELLOW + f"Config file {cfl} not found, creating it. Please restart the script\r"+ Style.RESET_ALL)
            print("------")
        except:
            print(Fore.RED + f"\nCan't create a config file ({cfl})\n"+ Style.RESET_ALL)  
            print("------\n")
            raise ImportError
        finally:
            exit(0)

# EXITING THE EXTERIOR VARIABLES DEFINITION PART
# -------------------------------
# ENTERING THE EXTERIOR VARIABLES MODIFICATION PART

if args.var:
    for key, value in EV.items(): # Adding the external variables to the argument parser
        print(f"pre-generating '{key}'")
        if type(value) != type([]):
            print( Fore.RED + f"----\nSkipping {key}: {value}\r" + Style.RESET_ALL)
            print(Fore.RED +f"IT MUST BE A LIST\n" + Style.RESET_ALL)
        elif len(value) < 2 :
            print( Fore.RED + f"----\nSkipping {key}: {value}\r" + Style.RESET_ALL)
            print( Fore.RED + f"A VALUE AND A COMMENT MUST BE PRESENT\n" + Style.RESET_ALL)
        else:
            parser.add_argument(f"--{key.lower().replace('_', '-')}", help=f"{value[1]}")
            globals()[key] = value[0]
    print(f"-\npre-generation finished\n-")

    j=0
    match={}
    change="o"
    for key, value in EV.items():
        nkey=key.lower().replace('_', '-')
        print(f"[{j}] {key}: {value[0]}\n{value[1]}\n")
        match[j]=key
        j+=1

    print("---------- ⬆️ variables ⬆️ ----------")

    while change=="o":
        i1=input("Which value do you want to change ?\n")
    
        while not (i1.isdigit() and (int(i1) < len(EV))): # Checking if the input is a number and if it is not too high 
            print("\nInput is not valid: Either not a number or number is too high")
            i1=input("Which value do you want to change ?\n")
        with open(cfl, "r+") as json_conf:
                data = load(json_conf)
                for k in range(len(match)):
                    if k == int(i1):
                        data[match.get(k)][0] =input(f"\r[{i1}] {match.get(k)}: ")
                        json_conf.seek(0)
                        dump(data, json_conf, indent=4)
                        json_conf.truncate()
        change=input("\nDo you to make another change ? [o/n]: ")
        while change not in ["o", "n"]:
            change=input("\nInput is not valid: It's not 'o' or 'n'\nDo you to make another change ? [o/n]: ")
        print()
    json_conf.close()
    #exit(0)

EV = load(open(cfl)) #EXTERIOR VARIABLES
for key, value in EV.items(): # Adding the external variables to the argument parser
    print(f"Generating '{key}'")
    if type(value) != type([]):
        print( Fore.RED + f"----\nSkipping {key}: {value}\r" + Style.RESET_ALL)
        print(Fore.RED +f"IT MUST BE A LIST\n" + Style.RESET_ALL)
    elif len(value) < 2 :
        print( Fore.RED + f"----\nSkipping {key}: {value}\r" + Style.RESET_ALL)
        print( Fore.RED + f"A VALUE AND A COMMENT MUST BE PRESENT\n" + Style.RESET_ALL)
    else:
        globals()[key] = value[0]
print(f"-\nGeneration finished\n-")


# EXITING THE EXTERIOR VARIABLES MODIFICATION PART
# -------------------------------
# ENTERING THE FUNCTIONS DEFINITION PART

def cm_to_px(x_cm, y_cm, dpi):
    m=0
    r=[0,0,0]
    for a in [x_cm, y_cm, dpi]:
        if type(a)==type("a"):
            r[m]=(float(str(a).replace(",",".")))
        elif ((type(a)!=type(0.1)) and (type(a)!=type(1))):
            print(Fore.RED + f"\nConversion from cm to px error:\n{a} is not a number\nIt's a {type(a)}\n" + Style.RESET_ALL)
            raise ValueError
        else:
            r[m]=a
        m+=1
    
    x_px = round(int(r[0] * r[2] / 2.54),-1)  # 1 inch = 2.54 cm
    y_px = round(int(r[1] * r[2] / 2.54),-1)
    return x_px, y_px

# EXITING THE FUNCTIONS DEFINITION PART
# -------------------------------
# ENTERING THE INTERNAL VARIABLES DEFINITION PART

i=0 # a counter 
c={} # dictionnary that will hold all the data for the cards
#Internal 'cards' Variables
XV=XK # X coordinate of the value
P_x=XK # X coordinate of the picture
A6=cm_to_px(canvasx,canvasy,dpi) # A6 format in pixels at 300 dpi
canvas_x = A6[0] # canvas width of an A6 format (IRL) with a DPI of 300 
canvas_y = A6[1] # canvas height of an A6 format (IRL) with a DPI of 300
h_font_size = 1 # starting font size for the heading
t_font_size = 1 # starting font size for the text
P=cm_to_px(Px,Py,dpi) # Photo format (3.5 x 4.5 cm) in pixels at 300 dpi
D=cm_to_px(Dx,Dy,dpi) # (0.5 x 0.5 cm) in pixels at 300 dpi
a=0 # a counter that will be used as the key of the dictionnary that will hold all the data for the cards

# EXITING THE INTERNAL VARIABLES DEFINITION PART
# -------------------------------
# ENTERING THE PRE-RUNTIME CHECK PART

try:
    df = read_csv(url) # object holding the spreadsheet
except:
    print(Fore.RED + f"\n{url}\n\nThis URL is either not a CSV file or not readible one\n"+ Style.RESET_ALL)
    raise ImportError

for t1 in [save_folder, picture_folder]: # Checking if the folders exist and creating them if they don't
    if not path.exists(f"./{t1}"):
        print(Fore.YELLOW + f"\n Folder ./{t1} not found, creating one\n"+ Style.RESET_ALL)
        try :
            makedirs(f"./{t1}")
        except:
            print(Fore.RED + f"\n Can't create folder ./{t1}\n"+ Style.RESET_ALL)
            raise ImportError

for t2 in [h_font_path, t_font_path]: # Checking if the font files exist
    if not path.isfile(f"{t2}"):
        print(Fore.RED + f"\n Font file '{t2}' not found\n"+ Style.RESET_ALL)
        raise ImportError
    h_font = ImageFont.truetype(h_font_path, h_font_size) # font object for the heading that hold the font and its size
    t_font = ImageFont.truetype(t_font_path, t_font_size) # font object for the text that hold the font and its size

for t3 in [bg, g_diam_b, g_diam_w]: # Checking if the files exist
    if not path.isfile(f"{t3}"):
        print(Fore.RED + f"\n File '{t3}' not found\n"+ Style.RESET_ALL)
        raise ImportError

# EXITING THE PRE-RUNTIME CHECK PART
# -------------------------------
# ENTERING THE IMPORT DATA PART

print("------")
print(df)
print("------\n")

while i < len(df):
    b={}
    # Next line is checking if the number of point is 0 (which means that the member either never came to the FabLab or didn't filled the form)
    if (df.loc[i][LQPS] == df.loc[i][LQPS]) and (df.loc[i][LQPS]!=0): # obj==obj is always false if obj is a NaN. Goes through Members with at least one point
        max_key_length = max(len(key) for key in df.loc[i].keys())
        for key,value in df.loc[i].items(): # Displaying the data and putting it in form
            if type(value) == numpy.int64: # if the value is a numpy 64 bit integer, it is converted to a standart python integer
                value = int(value)
            print("{:<{width}}: {}".format(key, value, width=max_key_length)) # printing the data
            b[key]= value # putting the data in the dictionnary that will hold all the data for this member
        b["Membres"]= df.loc[i]["Membres"] # adding the name of the current member to the dictionnary
        c[a]=b # putting the dictionnary of this member in the dictionnary that will hold all the data of all the users
        #print("b: {}".format(dumps(b, indent=4))) # printing the dictionnary of this member

    else: #If the member knows nothing
        print( Fore.RED +"\n {} KNOWS NOTHING\n".format(df.loc[i]["Membres"]) + Style.RESET_ALL) 
    if i < len(df)-1:
        print("---------- {}->{} ----------".format(str(i), str(i+1)))
    else:
        print("---------- {}-> {} ----------".format(str(i), "Cards making"))
    a += 1
    i += 1
#print("c: {}".format(dumps(c, indent=4))) # printing the dictionnary that holds all the dictionnaries of all the users


# EXITING THE IMPORTING DATA PART
# -------------------------------
# ENTERING THE CARD MAKING PART

# Create base canvas
image = Image.new('RGBA', (canvas_x, canvas_y), (255, 255, 255, 255))
draw = ImageDraw.Draw(image)

# Initializing variables counting the length of texts combinations
lenhdg= 0
lenkey= 0
lentxt= 0
# Initializing variables storing the longest text combination
maxlenhdg= [0,0]
maxlenkey= [0,0]
maxlentxt= [0,0]

# Find the longest text combination (in caracter)
for name, data in c.items():
    for key, value in data.items():
        pre_maxlen = lentxt
        pre_maxlenkey = lenkey
        pre_maxlenhdg = lenhdg

        lentxt = 0
        lenkey = 0
        lenhdg = 0

        TXTKEY='{}: '.format(key)
        if key == "Membres":
            TXTHDG='{}'.format(value)
        if key == "% Maitrise du FabLab" or "Maitrise du FabLab":
            TXTVALUE='{}'.format(value)
        else:
            TXTVALUE=''
        TXT=TXTKEY+TXTVALUE

        lentxt=len(TXT)
        lenkey=len(TXTKEY)
        lenhdg=len(TXTHDG)

        if lentxt > pre_maxlen:
            #print("TXT: {} | {} caracters".format(TXT, lentxt))
            #print("maxlentxt: {} | {}".format(maxlentxt[0], maxlentxt[1]))
            maxlentxt[0]=TXT
            maxlentxt[1]=lentxt
        if lenkey > pre_maxlenkey:
            #print("TXTKEY: {} | {} caracters".format(TXTVALUE, lenkey))
            #print("malxlenkey: {} | {}".format(maxlenkey[0], maxlenkey[1]))
            maxlenkey[0]=TXTKEY
            maxlenkey[1]=lenkey
        if lenhdg > pre_maxlenhdg:
            #print("TXTHDG: {} | {} caracters".format(TXTHDG, lenhdg))
            #print("maxlenhdg: {} | {}".format(maxlenhdg[0], maxlenhdg[1]))
            maxlenhdg[0]=TXTHDG
            maxlenhdg[1]=lenhdg


print("biggest lenght of HDG:"+ Fore.LIGHTCYAN_EX +f" \'{maxlenhdg[0]}\'"+ Style.RESET_ALL +f" | {maxlenhdg[1]} caracters")        
print("biggest lenght of KEY:"+ Fore.LIGHTCYAN_EX +f" \'{maxlenkey[0]}\'"+ Style.RESET_ALL +f" | {maxlenkey[1]} caracters")
print("biggest lenght of TXT:"+ Fore.LIGHTCYAN_EX +f" \'{maxlentxt[0]}\'"+ Style.RESET_ALL +f" | {maxlentxt[1]} caracters")

# Assigning the longest text combination to variables
HEADING=maxlenhdg[0]
KEY=maxlenkey[0]
TXT=maxlentxt[0]

# Initializing variables counting the size of the image of the longuest texts
sizehdg= 0
sizekey= 0
sizetxt= 0

# finding the font size of HEADING so it fits the desired width fraction of the card
while sizehdg < float(h_width_fraction)*(image.size[0]-int(XH)): # iterate until the header size is just larger than the criteria
    h_font_size += 1
    h_font = ImageFont.truetype(h_font_path, h_font_size)
    sizehdg = int(draw.textlength(HEADING, h_font))
    #print("sizehdg: {}x{} px".format(sizehdg, h_font_size))
#print("--")
# finding the font size of TEXT so it fits the desired width fraction of the card
while sizetxt < float(t_width_fraction)*(image.size[0]-int(XK)): # iterate until the text size is just larger than the criteria
    t_font_size += 1
    t_font = ImageFont.truetype(t_font_path, t_font_size)
    sizetxt= int(draw.textlength(TXT, t_font))
    #print("sizetxt: {}x{} px".format(sizetxt, t_font_size))


# de-increment to be sure it is less than criteria
h_font_size -= 1
t_font_size -= 1
h_font = ImageFont.truetype(h_font_path, h_font_size)
t_font = ImageFont.truetype(t_font_path, t_font_size)
sizehdg = int(draw.textlength(HEADING, h_font))
sizekey = int(draw.textlength(KEY, t_font))
sizetxt = int(draw.textlength(TXT, t_font))

# Printing the results
print("------")
print(f"maximum size of HEADER: {int(float(h_width_fraction)*image.size[0])} px")
print(f"size of HEADER: {sizehdg} px")
print(f"heigh of HEADER: {h_font_size} px")
print("---")
print(f"maximum size of TEXT: {int(float(t_width_fraction)*image.size[0])} pixels")
print(f"size of TEXT: {sizetxt} pixels")
print(f"heigh of TEXT: {t_font_size}")
print("------")

for name, data in c.items():
    image = Image.new('RGBA', (canvas_x, canvas_y), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    fond= Image.open(bg)
    fond = fond.convert("RGBA")
    image.paste(fond, (0, 0), fond)
    i=0
    for key, value in data.items():
        diam_w = Image.open(f"{g_diam_w}")
        diam_b = Image.open(f"{g_diam_b}")
        TXTKEY='{}: '.format(key)
        TXT=TXTKEY
        YK=int(GYK1)+(int(GYK2)*i) # Y coordinate of the key
        XV=int(XK)+int(sizekey) # X coordinate of the value
        YV=int(YK) # Y coordinate of the value
        rz=0
        rzd=0
        int_value=0
        #print("-")
        if key == picture_column: # Add the picture of the member
            name=str(value)
            pic_path=f"./{picture_folder}/{name}"
            #print(pic_path)
            if not path.isfile(pic_path):
                try:
                    pic_path=f"./{picture_folder}/default.png"
                    path.isfile(pic_path)
                except:
                    print(Fore.RED + f"\n Image {name}.png not found in \'./{picture_folder}\' folder.\nDefault photos could not be found\n"+ Style.RESET_ALL)
                    raise ImportError   
            img = Image.open(pic_path)        
            LPM=int(P[0]*float(redux1)) # Largeur Photo Maximum 3,5 cm a 300 dpi
            HPM=int(P[1]*float(redux1)) # Hauteur Photo Maximum 4,5 cm a 300 dpi
            LP=int(img.size[0]) # Largeur Photo
            HP=int(img.size[1]) # Hauteur Photo
            while int(LP*rz) < LPM and int(HP*rz) < HPM:# Resize the picture until it fits the maximum size
                rz+=0.01
            LP=int(LP*rz)
            HP=int(HP*rz)
            img = img.convert("RGBA")
            img = img.resize([LP, HP])
            image.paste(img, (int(P_x), int(P_y)), img)     
            #print("Photo: T[{}x{}]px - P[{}x{}]px w/ rz={}".format(LP, HP, img.size[0], img.size[1], rz)) 
        elif key == LQPS:
            #print("{:<{width}}: {}".format(key, ("%g" % (float(str(value).replace(",",".")))), width=max_key_length))
            #nvale= "%g" % (float(str(value).replace(",",".")))
            #draw.text((XV, YV), nvale, (0, 0, 0), font=t_font)
            #draw.text((XK, YK), TXT, (0, 0, 0), font=t_font)
            pass
        elif key == "Membres":
            l=0
            for r in value:
                l+=draw.textlength(r,h_font)
            #print("TITRE:{} P[x:{};y:{}]px - S[{}x]px".format(value, XH, YH, l))
            print(Fore.LIGHTGREEN_EX+f"{value}"+Style.RESET_ALL)
            draw.text((int(XH), int(YH)), value, (0, 0, 0), font=h_font)
            mbr="{}/{}.png".format(save_folder,value.replace(" ", "_"))
        else:
            #print("{} K[x:{};y:{}]px - V[x:{};y:{}]px".format(TXTKEY, XK, YK, XV, YV))
            draw.text((int(XK), int(YK)), TXT, (0, 0, 0), font=t_font) # Printing the key
            if type(value) != str and key!=LQPS:
                int_value=int(value)
                LDM=int(D[0]*float(redux2)) # Largeur Diamant Maximum
                HDM=int(D[1]*float(redux2)) # Hauteur Diamant Maximum 
                LD=int(diam_w.size[0]) # Largeur Photo
                HD=int(diam_w.size[1]) # Hauteur Photo
                while int(LD*rzd) < LDM and int(HD*rzd) < HDM:# Resize the picture until it fits the maximum size
                    #print(f"int(LD*rzd): {int(LD*rzd)} | int(LD*rzd): {int(HD*rzd)} | rzd: {rzd}")
                    rzd+=0.01
                LD=int(LD*rzd)
                HD=int(HD*rzd)  
                diam_w = diam_w.convert("RGBA")
                diam_b = diam_b.convert("RGBA")
                diam_w = diam_w.resize([LD, HD])
                diam_b = diam_b.resize([LD, HD])
                #print("D - T[{}x{}]px - P[{}x{}]px w/ rzd={}".format(LD, HD, diam_w.size[0], diam_w.size[1], rzd))
                for j in range(1, 5):
                    YD=YK+15
                    XD=int(XV+100*(j-1)) # X coordinate of the diamond
                    if j<=int_value:
                        d=diam_w
                        color="W"
                    else:
                        d=diam_b
                        color="B"
                    #print("D{} - [x:{};y:{}] [{}x{}]px - j:{} | value:{}".format(color,XD, YD, D.size[0], D.size[1], j,int_value))
                    image.paste(d,(XD, YD), d)
        i+=1
        
    
    print(f"saved in ./{mbr}")
    image.save(mbr,dpi=(int(dpi),int(dpi)), format="png")
    print("------")
