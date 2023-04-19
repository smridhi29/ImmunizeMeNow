"""
Frontend 
"""
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import pytz 
import requests

IST = pytz.timezone('Asia/Kolkata')
software_version='v1.1'

topleft_bg="#527c88"
topright_bg="#2e4450"

app= Tk()

# app geometry and components
app.geometry("700x480+600+300")
app.title(f"ImmunizeMeNow {software_version}")
app.iconbitmap("Images/vaccine.ico")
app.resizable(False, True)
app.config(background='#d7baad')

#adding frame
frame1 = Frame(app, height=120, width=180, bg=topleft_bg, bd=1, relief= FLAT)
frame1.place(x=0, y=0)
frame2 = Frame(app, height=120, width=520, bg=topright_bg, bd=1, relief= FLAT)
frame2.place(x=180, y=0)
frame3 = Frame(app, height=30, width=700, bg='black', bd=1, relief= FLAT)
frame3.place(x=0, y=120)

#entry box
pincode_text_var= StringVar()
pincode_text= Entry(app, width=11, bg='white', fg='black', font='verdana 11', textvariable=pincode_text_var)
pincode_text.place(x=220, y=40)
pincode_text['textvariable']=pincode_text_var

date_text_var= StringVar()
date_text= Entry(app, width=11, bg='white', fg='black', font='verdana 11', textvariable=date_text_var)
date_text.place(x=380, y=40)
date_text['textvariable']=date_text_var

#button
search_vaccine_image= PhotoImage(file="Images\search.png")
search_vaccine_btn= Button(app, bg=topright_bg, relief= RAISED, command ='', image= search_vaccine_image)
search_vaccine_btn.place(x=600, y= 25)


#Labels
label_date_now = Label(text="Current Date", bg= topleft_bg, font='verdana 12 bold')
label_date_now.place(x=20, y=40)

label_time_now = Label(text="Current Time", bg= topleft_bg, font='verdana 12')
label_time_now.place(x=20, y=60)

label_pincode = Label(text="Pincode", bg= topright_bg, font='verdana 11', fg='white')
label_pincode.place(x=220, y=15)

label_date = Label(text="Date", bg= topright_bg, font='verdana 11', fg='white')
label_date.place(x=380, y=15)

label_dateformat = Label(text="[dd-mm-yyyy]", bg= topright_bg, font='verdana 7', fg='white')
label_dateformat.place(x=420, y=18)

label_search_vacc = Label(text="Search \nAvailable Vaccine", bg= topright_bg, font='verdana 7', fg='white')
label_search_vacc.place(x=570, y=70)

label_head_result = Label(text=" Status       \tCentre-Name\t              Age-Group    Vaccine       Dose_1     Dose_2     Total", bg = 'black', fg='white', font = 'Verdana 8 bold')
label_head_result.place(x=10, y=125)

#textbox= RESULTS
result_box_status= Text(app, height=20, width=8, bg='#d7baad', fg='#d7baad', relief=FLAT, font='verdana 10')
result_box_status.place(x=3, y=152)

result_box_centre= Text(app, height=20, width=30, bg='#d7baad', fg='#d7baad', relief=FLAT, font='verdana 10')
result_box_centre.place(x=75, y=152)

result_box_age= Text(app, height=20, width=8, bg='#d7baad', fg='#d7baad', relief=FLAT, font='verdana 10')
result_box_age.place(x=330, y=152)

result_box_vacc= Text(app, height=20, width=10, bg='#d7baad', fg='#d7baad', relief=FLAT, font='verdana 10')
result_box_vacc.place(x=400, y=152)

result_box_d1= Text(app, height=20, width=7, bg='#d7baad', fg='#d7baad', relief=FLAT, font='verdana 10')
result_box_d1.place(x=490, y=152)

result_box_d2= Text(app, height=20, width=7, bg='#d7baad', fg='#d7baad', relief=FLAT, font='verdana 10')
result_box_d2.place(x=555, y=152)

result_box_d1d2= Text(app, height=20, width=7, bg='#d7baad', fg='#d7baad', relief=FLAT, font='verdana 10')
result_box_d1d2.place(x=630, y=152)

#Defininf Functions
def update_clock():
    raw_TS =datetime.now(IST)
    date_now=raw_TS.strftime("%d %b %Y")
    time_now=raw_TS.strftime("%H:%M:%S %p")
    label_date_now.config(text= date_now)
    label_time_now.config(text=time_now)
    label_time_now.after(1000, update_clock)
update_clock()

def insert_today_date():
    raw_TS= datetime.now(IST)
    formatted_now=raw_TS.strftime("%d-%m-%y")
    date_text_var.set(formatted_now)
#checkbox
chkbox_var= IntVar()
chkbox= Checkbutton(app, text='Today', bg=topright_bg, fg='white', variable=chkbox_var, onvalue=1, offvalue= 0, command= insert_today_date)
chkbox.place(x=375, y=65)

def search_vacc_avail():
    clear_resultbox()
    PINCODE= pincode_text_var.get().strip()
    DATE= date_text_var.get()
    resp_JSON= refresh_api_call(PINCODE, DATE)

    try:
        if len(resp_JSON['sessions'])==0:
            messagebox.showinfo("Vaccine not available for the given date")

        for sess in resp_JSON['sessions']:
            age_limit           = sess['min_age_limit']
            center_name         = sess['name']
            pincode             = sess['pincode']
            vaccine_name        = sess['vaccine']
            available_capacity  = sess['available_capacity']
            qnty_dose_1         = sess['available_capacity_dose1']
            qnty_dose_2         = sess['available_capacity_dose2']
            slot_date           = sess['date']

            if available_capacity > 0:
                curr_status = 'Available'
            else:
                curr_status = 'NA'
            
            if age_limit == 45:
                age_grp = '45+'
            else:
                age_grp = '18-44'
            
            result_box_status.insert(END, f"{curr_status:^6s}")
            result_box_status.insert(END,"\n")
            result_box_centre.insert(END, f"{center_name:<30.29s}")
            result_box_centre.insert(END,"\n")
            result_box_age.insert(END, f"{age_grp:<6s}")
            result_box_age.insert(END,"\n")
            result_box_vacc.insert(END, f"{vaccine_name:<8s}")
            result_box_vacc.insert(END,"\n")
            result_box_d1.insert(END, f"{qnty_dose_1:>5}")
            result_box_d1.insert(END,"\n")
            result_box_d2.insert(END, f"{qnty_dose_2:>5}")
            result_box_d2.insert(END,"\n")
            result_box_d1d2.insert(END, f"{available_capacity:<5}")
            result_box_d1d2.insert(END,"\n")
    except KeyError as KE:
        messagebox.showerror("ERROR","No Available center(s) for the given Pincode and date")
        print (pincode_text_var.get())

url= 'https://ipinfo.io/postal'
def get_pincode(url):
    return requests.get(url).text

def fill_pincode_with_radio():
    curr_pincode= get_pincode(url)
    pincode_text_var.set(curr_pincode)


#Radio button
current_loc_var= StringVar()
current_loc= Radiobutton(app, text="Current Location", bg= topright_bg, fg='white',variable=current_loc_var, value=current_loc_var, command=fill_pincode_with_radio)
current_loc.place(x=215, y=65)

def refresh_api_call(PINCODE, DATE):
    header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
    request_link =f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={PINCODE}&date={DATE}"
    response = requests.get(request_link, headers=header)
    return response.json()

def clear_resultbox():
    result_box_status.delete('1.0', END)
    result_box_vacc.delete('1.0', END)
    result_box_age.delete('1.0', END)
    result_box_centre.delete('1.0', END)
    result_box_d1.delete('1.0', END)
    result_box_d2.delete('1.0', END)
    result_box_d1d2.delete('1.0', END)

app.mainloop()