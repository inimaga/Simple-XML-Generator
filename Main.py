"""/
    Simple XML Generator - By Issa Nimaga
    Custom Gui Application developed for the marketing department of STL Partners
/"""
import PySimpleGUI as sg
from os import path

# Theme specification
sg.theme('LightBlue6')	# Add a touch of color

"""
# ------ Menu Definition ------ #      
menu_def = [['File', ['Exit']],      
            ['About'], ]    
"""

hfs = 15 #hfs is short of horizontal field spacing
# All the stuff inside your window.
layout = [  
            #[sg.Menu(menu_def, tearoff=True)], 
            #[sg.Text('Please enter details of the files below:', size=(45, 1), font=("Arial", 14), justification="center")],
            [sg.Text('Title', size=(hfs, 1)), sg.InputText(key='title')],
            [sg.Text('Description', size=(hfs, 1)), sg.Multiline(key='des')],
            [sg.Text('Document type', size=(hfs, 1)), sg.Radio('Report', "RADIO1", default=True, key='radioReport'), sg.Radio('Other', "RADIO1")],
            [sg.Text('Module 1', size=(hfs, 1)), sg.InputText(key='mod1')],
            [sg.Text('Module 2', size=(hfs, 1)), sg.InputText(key='mod2')],

            #Arianet theme section
            [sg.Text('Arianet Theme', size=(hfs, 1)) , sg.Frame(layout=[            
            [sg.Checkbox('Enterprise ICT', key='AT_cb1'), sg.Checkbox('Entreprise IT (incl Cloud)', key='AT_cb2')],
            [sg.Checkbox('Enterprise customer experience', key='AT_cb3'), sg.Checkbox('Small & medium-sized businesses', key='AT_cb4')],
            [sg.Checkbox('Consumer access & communications', key='AT_cb5'), sg.Checkbox('Consumer contents and applications', key='AT_cb6')],
            [sg.Checkbox('Consumer commerce & transactions', key='AT_cb7'), sg.Checkbox('Devices', key='AT_cb8')],
            [sg.Checkbox('Customer/User experience', key='AT_cb9'), sg.Checkbox('IoT incl. M2M', key='AT_cb10')],
            [sg.Checkbox('Digital society, ecosystems & partnerships', key='AT_cb11'), sg.Checkbox('Public network infrastructure', key='AT_cb12')],
            [sg.Checkbox('Telecom software (OSS/BSS)', key='AT_cb13'), sg.Checkbox('Wholesale', key='AT_cb14')],
            [sg.Checkbox('Global market evolution, regulation, competition, strategic partnerships, …', key='AT_cb15')
            ]],title='(Select a Max of 3 relevant themes)')],
            #
            [sg.Text('Companies', size=(hfs, 1)), sg.InputText(key='company')],
            [sg.Text('Countries', size=(hfs, 1)), sg.InputText(key='country')],
            [sg.Text('Keywords', size=(hfs, 1)), sg.InputText(key='kwds')],
            [sg.Text('Author', size=(hfs, 1)), sg.InputText(key='author')],
            [sg.Text('Publication Date', size=(hfs, 1)), sg.CalendarButton('Choose Date', target='calInput', no_titlebar=False), sg.Text('Undefined', size=(hfs*2, 1), key="dateShown"), sg.InputText(key='calInput', visible=False, enable_events=True)],
            #NB: For some reason, the attribute 'no_titlebar' is necessary. The program will not work otherwise
            [sg.Text('Document ID', size=(hfs, 1)), sg.InputText( key='docIDinput', enable_events=True )],
            [sg.Text('Files', size=(hfs, 1)), sg.Text('undefined.pdf', key="fileName", size=(hfs*2, 1))],
            [sg.Text('Publisher', size=(hfs, 1)), sg.InputText('STL Partners',key='publisher')],
            [sg.Text('Save location', size=(hfs, 1)), sg.FolderBrowse(target='-USER FOLDER-'), sg.Text('(Same as folder containing application by default)', key="pathShown"), sg.InputText(path.dirname(__file__),key='-USER FOLDER-', visible=False, enable_events=True)],
            [sg.Text(" ")],
            [sg.Button('Generate XML File'), sg.Button('Exit')] ]

# Creation of the Window
xml_icon = path.join(path.dirname(__file__),'xml.ico')
window = sg.Window('Simple XML Generator - (Custom GUI app for STL Partners) - v0.1', layout, icon=xml_icon)
#saveLocation = path.join(path.dirname(__file__), r'generated_file.xml') #default save location

fileName  = "generated.xml" #Variable representing the name of file to save

#Dictionary representing the properties of the XML
documentProperties = {
    "documentid":"",
    "title":"",
    "author":"",
    "publisher":"",
    "pubdate":"",
    "doctype":"",
    "description":"",
    "module1":"",
    "module2":"",
    "themearianet":"",
    "companies":"",
    "countries":"",
    "keywords":"",
    "files":""
}
#
def updateDocProperties():
    documentProperties["documentid"] = values['docIDinput']
    documentProperties["title"] = values['title']
    documentProperties["description"] = values['des'].rstrip('\n')
    documentProperties["module1"] = values['mod1']
    documentProperties["module2"] = values['mod2']
    documentProperties["companies"] = values['company']
    documentProperties["countries"] = values['country']
    documentProperties["keywords"] = values['kwds']
    documentProperties["author"] = values['author']
    documentProperties["publisher"] = values['publisher']
    documentProperties["files"] = values['docIDinput']+".pdf"
    #saveLocation = values['-USER FOLDER-']

    #Logic for the radio button
    if(values['radioReport']):
        documentProperties["doctype"] = 'Report'
    else:
        documentProperties["doctype"] = 'Other'
    #

    #Logic for the Arianet checkboxes
    selectedBoxes = []
    for i in range (1, 15):
        key2search = 'AT_cb' + str(i)
        if (values[key2search]):
            selectedBoxes.append(i)
    documentProperties["themearianet"] = ",".join(str(w) for w in selectedBoxes)
    #

def formatDictionaryForSaving(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>')
    file.write('\n<root>')
    
    for key in documentProperties:
        file.write('\n    <' + key + '>')
        file.write(documentProperties[key])
        file.write('</' + key + '>')

    file.write('\n</root>')
    file.close()

#Function for saving xml file
def save_XML(saveLocation, dict):
    with open(saveLocation, 'w') as f:
        formatDictionaryForSaving(f)
    sg.popup('XML generated!')

def formatDateForXML(date):
    displayDate = date[:-9]
    pubdate= displayDate.replace("-","")
    documentProperties["pubdate"] = pubdate

    return displayDate

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Exit'):	# if user closes window or clicks cancel
        break

    elif event == "-USER FOLDER-":
        window['pathShown'].update(values['-USER FOLDER-'])
    elif event == "calInput":
        window['dateShown'].update(formatDateForXML(values['calInput']))
        window['docIDinput'].update(documentProperties["pubdate"]+'001')
        window['fileName'].update(documentProperties["pubdate"]+'001'+".pdf")

    elif event == "Generate XML File":
        updateDocProperties()
        fileName = documentProperties["documentid"] + '.xml'
        saveLocation = path.join(values['-USER FOLDER-'], fileName)
        save_XML(saveLocation, documentProperties)

    elif event == 'docIDinput' and values['docIDinput'] and values['docIDinput'][-1] not in ('0123456789.'):
        # if last character in input element is invalid, remove it
        window['docIDinput'].update(values['docIDinput'][:-1])
        #print(documentProperties)
    if event == 'docIDinput':
        window['fileName'].update(values['docIDinput']+".pdf")

window.close()