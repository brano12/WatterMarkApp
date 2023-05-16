import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import Image, ImageDraw, ImageFont, ImageTk

FONT_NAME = "arial"
SIZE = 90
COLOR = (255, 255, 255)
OPAC = (255,)

####################################### Functions for buttons and etc. #################################################
#print(type(COLOR))
class ClassToStoreReturnedVariable:
    def __init__ (self):
        self.returnedVariable = None

    def returnVariable (self, x):
        self.returnedVariable = x


retVar = ClassToStoreReturnedVariable()
retVarPil = ClassToStoreReturnedVariable()
retVarSave = ClassToStoreReturnedVariable()

def resize_image(kanvas):
    if kanvas.size[0] >= kanvas.size[1]:
        if kanvas.size[0] <= 700:
            basewidth = kanvas.size[0]
        else:
            basewidth = 900
    else:
        if kanvas.size[1] <= 900:
            basewidth = kanvas.size[0]
        else:
            basewidth = 500
    wpercent = (basewidth / float(kanvas.size[0]))
    hsize = int(float(kanvas.size[1]) * float(wpercent))
    return kanvas.resize((basewidth, hsize), Image.LANCZOS)


def select_file():

    filetypes = (
        ('image files', ('.png', '.jpg')),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    if not filename:

        return
    showinfo(
        title='Selected File',
        message=filename
    )
    # opening image with PIL
    img = Image.open(filename)
    #creating value we will work with behind the scene for adjusting the watermark
    retVarPil.returnVariable(img)
    # accomodating pictures dimensions and saving it to TK format
    tk_img = ImageTk.PhotoImage(resize_image(img))
    retVar.returnVariable(tk_img)
    uploadedimagelabel.config(image=retVar.returnedVariable, width=resize_image(img).size[0], height=resize_image(img).size[1])

def font_func(event):
    global FONT_NAME
    font_dict = {"Arial": "arial", "Arial Italic": "ariali", "Arial Bold":"arialbd", "Arial Black": "ariblk", "Impact": "impact",
                 "Script MT Bold": "SCRIPTBL", "Calibri": "calibri", "Calibri Italic" : "calibrii", "Calibri Bold":"calibrib",
                 "Calibri Bold Italic" : "calibriz"}
    FONT_NAME = font_dict.get(selected_font.get())

def size_func(event):
    global SIZE
    SIZE = selected_size.get()

def color_func(event):
    global COLOR
    color_dict = {'black': (0,0,0), 'gray': (160, 160, 160), 'brown': (102, 51, 0), 'blue': (0, 128, 255), 'purple':(153, 51, 255),
                  'green': (0,153,76), 'red':(255,0,0), 'yellow':(255,255,0), 'white':(255,255,255), 'silver':(192,192,192),
                  'gold':(255,153,51), 'orange': (255, 128, 0)}
    COLOR = color_dict.get(selected_color.get())

def opac_func(event):
    global OPAC
    opac_dict = {100: (255,), 75: (192,), 50: (127,), 25: (65,), 0: (0,)}
    OPAC = opac_dict.get(selected_opac.get())


def save():
    file = filedialog.asksaveasfile(mode='w',
                                    defaultextension='*.*',
                                    filetypes=(('JPG file', '*.jpg'), ('PNG file', '*.png'),
        ('All files', '*.*')))
    if file:
        retVarSave.returnedVariable.save(file.name)
    # Save watermarked image
    # im.save('watermark.jpg')

def help():
    tkinter.messagebox.showinfo(title="Help", message="Hello\n\n-upload photo with Open button.\n-write text for your watermark"
                                                      "\n-choose your font, size and opacity if wanted\n-save changes on the picture"
                                                        "to the new file.")
def about():
    tkinter.messagebox.showinfo(title="About", message="Desktop Watermark App 1.0\n\nFree to share\n\nCreated by\nBranislav Noskovič\n2023.")

def confirm():
    img=retVarPil.returnedVariable

    if img == None:
        showinfo(
            title='Warning',
            message='Please upload file first'
        )
        return
    else:

        width, height = img.size

        ############# opacity part ################
        img = img.convert('RGBA')
        opaque_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
        ########################################

        draw = ImageDraw.Draw(opaque_img)
        text = wm_entry.get()

        font = ImageFont.truetype(FONT_NAME, SIZE)
        textwidth, textheight = draw.textsize(text, font)
        # calculate the x,y coordinates of the text
        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin

        # draw watermark in the bottom right corner
        draw.text((x, y), text, font=font, fill= (COLOR+(OPAC)))
        combined = Image.alpha_composite(img, opaque_img)

        ######### this is for pointing adjusted picture object to value for file saving purpose ###############
        retVarSave.returnVariable(combined.convert('RGB'))
        #### this is for displaying the picture in the app, we have to point it by another object attribute due to garbage disposal propterty of python ####
        tk_img = ImageTk.PhotoImage(resize_image(combined))
        retVar.returnVariable(tk_img)
        uploadedimagelabel.config(image=retVar.returnedVariable, width=resize_image(img).size[0],
                                  height=resize_image(img).size[1])
def reset_combo():
    global FONT_NAME
    global SIZE
    global COLOR
    global OPAC
    font_cb.current(0)
    opac_cb.current(0)
    size_cb.current(7)
    color_cb.current(9)
    wm_entry.delete(0,tkinter.END)
    FONT_NAME = "arial"
    SIZE = 90
    COLOR = (255, 255, 255)
    OPAC = (255,)
    confirm()

########################## GUI Section ############################################################

window = tkinter.Tk()
window.title("Image Watermarking Desktop App")
window.config(padx=20, pady=0, bg="white")

################################################# LEFT PANEL ###########################################################

canvas = tkinter.Canvas(width=150, height=60, bg="white", highlightthickness=0)
logo_img = ImageTk.PhotoImage(Image.open("logo.jpg"))
canvas.create_image(80, 30, image=logo_img)
canvas.grid(row=0,column=0)

open_instruction_label = tkinter.Label(text="File:", bg='#fff')
open_instruction_label.grid(row=2, column=0, sticky="N", padx=(0,50))

open_button = tkinter.Button(width=10, text="Open", command=select_file)
open_button.grid(row=3, column=0)

save_button = tkinter.Button(width=10,text="Save", command=save)
save_button.grid(row=4, column=0, pady=(0,400))

help_button = tkinter.Button(width=10,text="Help", command=help)
help_button.grid(row=5, column=0)

about_button = tkinter.Button(width=10,text="About", command=about)
about_button.grid(row=6, column=0)


################################################## DISPLAY #############################################################

uploadedimagelabel = tkinter.Label(width=130, height=40)
uploadedimagelabel.grid(padx=0, pady=10, rowspan=5, row=2, column=1, columnspan=7)

################################# FIRST COLUMN #################################

instruction_label = tkinter.Label(text="Your watermark text:", bg='#fff')
instruction_label.grid(row=0, column=1)

wm_entry = tkinter.Entry(width=20)
wm_entry.grid(row=1, column=1)


################################################## SECOND COLUMN #######################################################

font_label = tkinter.Label(text="Font:", bg='#fff')
font_label.grid(row=0, column=2, sticky= "W")

size_label = tkinter.Label(text="Size in pt.:", bg='#fff')
size_label.grid(row=1, column=2, sticky= "W")

################################################## THIRD COLUMN #######################################################

selected_font = tkinter.StringVar()
font_cb = ttk.Combobox(textvariable=selected_font)
# get first 3 letters of every month name
font_cb['values'] = ["Arial", "Arial Italic", "Arial Bold", "Arial Black", "Calibri", "Calibri Italic", "Calibri Bold",
                 "Calibri Bold Italic", "Script MT Bold"]
# prevent typing a value
font_cb['state'] = 'readonly'
font_cb.current(0)
font_cb.grid(row=0, column=3, sticky= "W")
font_cb.bind('<<ComboboxSelected>>', font_func)


selected_size = tkinter.IntVar()
size_cb = ttk.Combobox(textvariable=selected_size)
# get first 3 letters of every month name
size_cb['values'] = [10, 20, 30, 40, 50, 60, 70, 90, 100, 120]
# prevent typing a value
size_cb['state'] = 'readonly'
size_cb.current(7)
size_cb.grid(row=1, column=3, sticky= "W")
size_cb.bind('<<ComboboxSelected>>', size_func)

################################################ FOURTH COLUMN ##########################################################
color_label = tkinter.Label(text="Color:", bg='#fff')
color_label.grid(row=0, column=4, sticky="W")

opacity_label = tkinter.Label(text="Opacity?", bg='#fff')
opacity_label.grid(row=1, column=4, sticky= "W")

################################################ FOURTH COLUMN ##########################################################
selected_color = tkinter.StringVar()
color_cb = ttk.Combobox(textvariable=selected_color)
# get first 3 letters of every month name
color_cb['values'] = ['black', 'gray', 'brown', 'blue', 'purple', 'green', 'red', 'orange', 'yellow', 'white', 'silver', 'gold']
# prevent typing a value
color_cb['state'] = 'readonly'
color_cb.current(9)
color_cb.grid(row=0, column=5, sticky= "W")
color_cb.bind('<<ComboboxSelected>>', color_func)

selected_opac = tkinter.IntVar()
opac_cb = ttk.Combobox(textvariable=selected_opac)
# get first 3 letters of every month name
opac_cb['values'] = [100, 75, 50, 25, 0]
# prevent typing a value
opac_cb['state'] = 'readonly'
opac_cb.current(0)
opac_cb.grid(row=1, column=5, sticky= "W")
opac_cb.bind('<<ComboboxSelected>>', opac_func)

############################################ SIXTH COLUMN #############################################################

sign_label = tkinter.Label(text="Apply changes:", bg='#fff')
sign_label.grid(row=0, column=6, sticky= "W")

confirm_button = tkinter.Button(width=10, text="Confirm", command=confirm)
confirm_button.grid(row=0, column=7)

sign_label = tkinter.Label(text="Reset values:", bg='#fff')
sign_label.grid(row=1, column=6, sticky= "W")

reset_button = tkinter.Button(width=10,text="Reset", command=reset_combo)
reset_button.grid(row=1, column=7)

window.mainloop()
