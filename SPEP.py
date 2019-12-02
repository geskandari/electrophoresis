import sys
#import pandas as pd
import psycopg2
import tkinter as tk
from tkinter import messagebox
import calendar
import datetime



class Calendar:
    def __init__(self, parent, values):
        self.values = values
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.wid = []
        self.day_selected = 1
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''

        self.setup(self.year, self.month)

    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            self.wid.remove(w)

    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1

        self.clear()
        self.setup(self.year, self.month)

    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

        self.clear()
        self.setup(self.year, self.month)

    def selection(self, day, name):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name

        # data
        self.values['day_selected'] = day
        self.values['month_selected'] = self.month
        self.values['year_selected'] = self.year
        self.values['day_name'] = name
        self.values['month_name'] = calendar.month_name[self.month_selected]

        self.clear()
        self.setup(self.year, self.month)

    def setup(self, y, m):
        left = tk.Button(self.parent, text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)

        header = tk.Label(self.parent, height=2, text='{}   {}'.format(calendar.month_abbr[m], str(y)))
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)

        right = tk.Button(self.parent, text='>', command=self.go_next)
        self.wid.append(right)
        right.grid(row=0, column=5)

        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, text=name[:3])
            self.wid.append(t)
            t.grid(row=1, column=num)

        for w, week in enumerate(self.cal.monthdayscalendar(y, m), 2):
            for d, day in enumerate(week):
                if day:
                    b = tk.Button(self.parent, width=1, text=day,
                                  command=lambda day=day: self.selection(day, calendar.day_name[(day - 1) % 7]))
                    self.wid.append(b)
                    b.grid(row=w, column=d)

        sel = tk.Label(self.parent, height=2, text='{} {} {} {}'.format(
            self.day_name, calendar.month_name[self.month_selected], self.day_selected, self.year_selected))
        self.wid.append(sel)
        sel.grid(row=8, column=0, columnspan=7)

        ok = tk.Button(self.parent, width=5, text='OK', command=self.kill_and_save)
        self.wid.append(ok)
        ok.grid(row=9, column=2, columnspan=3, pady=10)

    def kill_and_save(self):
        global rows
        dateObject = datetime.date(self.year_selected, self.month_selected, self.day_selected)

        con = psycopg2.connect(
            host="",#DATABASE HOSTNAME
            dbname="",#DATABASE DB NAME
            port="5432",#DATABASE PORT
            user="",#DATABASE USERNAME
            password="")#DATABASE PASSWORD
        cur = con.cursor()
        cur.execute("""select data_analisi, data_prel, seq, programma, eta, pt,
            nome_1, fraz_1, nome_2, fraz_2, nome_3, fraz_3, nome_4, fraz_4, nome_5, fraz_5
            from anagrafica where programma = 'J' AND data_analisi = (%s)""", [dateObject])
        rows = cur.fetchall()
        cur.close()
        con.close()
        Date = tk.Label(frame, text=dateObject, font=20)
        Date.place(relx=0.40, rely=0, relwidth=0.20, relheight=0.1)
        self.parent.destroy()
        resetTK()


rowNumber = -1
rows = {}
X = ""
H = 'No'
B = 'No'

def resetTK():
    rowNumber = -1
    nextRow()


def pickDate():
    calendarData = {}
    calendarPopupFrame = tk.Toplevel()
    calendarObject = Calendar(calendarPopupFrame, calendarData)

def HY():
    global H
    H = 'Yes'
    updateTK()


def HN():
    global H
    H = 'No'
    updateTK()


def BY():
    global B
    B = 'Yes'
    updateTK()


def BN():
    global B
    B = 'No'
    updateTK()


def updateTK():
    global rowNumber, rows
    History = tk.Label(frame, text='Does patient ' + str(rowNumber + 1) + '  have a previous history?', font=20)
    History.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.2)
    newComment = ""
    try:
        newComment = CM(rows[rowNumber])
    except:
        newComment = "An error occurred when trying to create the comment"
    comment.delete('1.0', tk.END)
    comment.insert(tk.END, str('Case ' + str(rowNumber + 1) + ':  ' + newComment))


def nextRow():
    global rowNumber
    global H
    global B
    if rowNumber == len(rows) - 1:
        return
    rowNumber = rowNumber + 1
    var1.set('no')
    var2.set('no')
    H = 'No'
    B = 'No'
    updateTK()


def prevRow():
    global rowNumber
    global H
    global B
    if rowNumber == 0:
        return
    rowNumber = rowNumber - 1
    var1.set('no')
    var2.set('no')
    H = 'No'
    B = 'No'
    updateTK()


def close():
    global root
    root.destroy()


def CM(row):
    data_analisi = row[0]
    data_prel = row[1]
    seq = row[2]
    programma = row[3]
    eta = row[4]
    pt = row[5]
    nome_1 = row[6]
    patientRelAlbumin = row[7]
    nome_2 = row[8]
    patientRelAlpha1 = row[9]
    nome_3 = row[10]
    patientRelAlpha2 = row[11]
    nome_4 = row[12]
    patientRelBeta = row[13]
    nome_5 = row[14]
    patientRelGamma = row[15]

    eta = 64
    pt = 6.3

    albuminRLow = 55.8#59.8-done
    albuminRHigh = 66.1#72.4-done
    albuminALow = 3.51#4-done
    albuminAHigh = 5.42#5.3-done

    alpha1RLow = 2.9#1-done
    alpha1RHigh = 4.9#3.2-done
    alpha1ALow = .18#.1-done
    alpha1AHigh = .4#.25-done

    alpha2RLow = 7.1#7.4-done
    alpha2RHigh = 11.8#12.6-done
    alpha2ALow = .44#.58-done
    alpha2AHigh = .96#.84-done

    betaRLow = 8.4#7.5-done
    betaRHigh = 13.1#12.9-done
    betaALow = .52#.5-done
    betaAHigh = 1.07#1.1-done

    gammaRLow = 11.1#8-done
    gammaRHigh = 18.8#15.8-done
    gammaALow = .7#.6-done
    gammaAHigh = 1.54#1.3-done

    proteinALow = 6.2

    patientAbsAlbumin = (patientRelAlbumin * pt) / 100
    patientAbsAlpha1 = (patientRelAlpha1 * pt) / 100
    patientAbsAlpha2 = (patientRelAlpha2 * pt) / 100
    patientAbsBeta = (patientRelBeta * pt) / 100
    patientAbsGamma = (patientRelGamma * pt) / 100

    if H == 'Yes':
        X = 'Compared to the study dated XXX, the previously identified monoclonal XXX band has decreased OR increased from XX g/dL to XX g/dL. Uninvolved gamma globulins are XXX decreased. No other significant changes are noted.'
    elif B == 'Yes':
        X = 'Abnormal serum protein study due to the presence of a band in the gamma region that immunofixes as monoclonal XXXXXX. This band is present at a concentration of XXX g/dL. Uninvolved gamma globulins are XXX decreased XXX and no other significant abnormalities are noted. These results are consistent with a monoclonal gammopathy of undetermined significance (MGUS) although a B-cell dyscrasia is not excluded.'
    else:
        if (patientAbsAlbumin >= albuminALow) & (patientAbsAlbumin <= albuminAHigh) & (patientAbsAlpha1 > alpha1ALow) & (
                patientAbsAlpha1 <= alpha1RHigh) & (patientAbsAlpha2 > alpha2ALow) & (patientAbsAlpha2 < alpha2AHigh) & (
                patientAbsBeta > betaALow) & (patientAbsBeta < betaAHigh) & (patientAbsGamma > gammaALow) & (
                patientAbsGamma < gammaAHigh):
            X = 'A normal serum protein study.'
        elif (patientAbsAlbumin < albuminALow) & (pt >= proteinALow) & (patientRelAlpha1 > alpha1RHigh) & (patientRelAlpha2 > alpha2RHigh):
            X = 'Albumin is decreased while the relative concentrations of alpha-1 globulins and alpha-2 globulins are increased indicating an acute phase response to infection, inflammation or tissue injury.'
        elif (patientAbsAlbumin < albuminALow) & (pt < proteinALow) & (patientRelAlpha1 > alpha1RHigh) & (patientRelAlpha2 > alpha2RHigh):
            X = 'Total protein and albumin are decreased while the relative concentrations of alpha-1 globulins and alpha-2 globulins are increased indicating an acute phase response to infection, inflammation or tissue injury.'
        elif (patientAbsAlbumin < albuminALow) & (pt >= proteinALow) & (patientRelAlpha1 > alpha1RHigh) & (patientRelAlpha2 >= alpha2RLow) & (patientRelAlpha2 <= alpha2RHigh):
            X = 'Albumin is decreased while the relative concentration of alpha-1 globulins is increased indicating an acute phase response to infection, inflammation or tissue injury.'
        elif (patientAbsAlbumin < albuminALow) & (pt < proteinALow) & (patientRelAlpha1 > alpha1RHigh) & (patientRelAlpha2 >= alpha2RLow) & (patientRelAlpha2 <= alpha2RHigh):
            X = 'Total protein and albumin are decreased while the relative concentration of alpha-1 globulins is increased indicating an acute phase response to infection, inflammation or tissue injury.'
        elif (patientAbsAlbumin < albuminALow) & (pt >= proteinALow) & (patientAbsGamma > gammaAHigh):
            X = 'Albumin is decreased while there is diffuse (polyclonal) increase in gamma globulins indicating a chronic disease pattern.'
        elif (patientAbsAlbumin >= albuminALow) & (pt >= proteinALow) & (patientAbsGamma > gammaAHigh):
            X = 'There is a diffuse (polyclonal) increase in gamma globulins suggesting a chronic immune response or chronic disease pattern.'
        elif (patientAbsAlbumin < albuminALow) & (pt >= proteinALow) & (patientRelAlpha1 > alpha1RHigh) & (patientRelAlpha2 > alpha2RHigh) & (patientAbsGamma < gammaAHigh):
            X = 'Albumin is decreased while gamma globulins are diffusely increased and alpha-1 globulins and alpha-2 globulins are relatively increased indicating a concomitant acute phase response and chronic disease pattern.'
        elif (patientAbsAlbumin < albuminALow) & (pt < proteinALow) & (patientRelAlpha1 > alpha1RHigh) & (patientRelAlpha2 > alpha2RHigh) & (patientAbsGamma > gammaAHigh):
            X = 'Total protein and albumin are decreased while gamma globulins are diffusely increased and alpha-1 globulins and alpha-2 globulins are relatively increased indicating a concomitant acute phase response and chronic disease pattern.'
        elif (eta >= 65) & (patientAbsAlbumin >= albuminALow) & (pt >= proteinALow) & (patientAbsAlpha1 > alpha1ALow) & (
                patientAbsAlpha1 <= alpha1RHigh) & (patientAbsAlpha2 > alpha2AHigh):
            X = 'Increased alpha-2 globulins may be due to increased haptoglobin in an acute phase response, increased alpha-2 macroglobulin in diabetes mellitus or may be a nonspecific finding most common in the elderly.'
        elif (eta < 65) & (patientAbsAlbumin >= albuminALow) & (pt >= proteinALow) & (patientAbsAlpha1 > alpha1ALow) & (
                patientAbsAlpha1 <= alpha1RHigh) & (patientAbsAlpha2 > alpha2AHigh):
            X = 'Increased alpha-2 globulins may be due to increased haptoglobin in an acute phase response or increased alpha-2 macroglobulin in diabetes mellitus.'
        elif (eta >= 65) & (patientAbsAlbumin < albuminALow) & (pt >= proteinALow):
            X = 'Albumin is decreased suggesting protein malnutrition although this may be a normal finding in the elderly.'
        elif (eta < 65) & (patientAbsAlbumin < albuminALow) & (pt >= proteinALow):
            X = 'Albumin is decreased suggesting protein malnutrition.'
        elif (eta >= 65) & (patientAbsAlbumin < albuminALow) & (pt < proteinALow):
            X = 'Total protein and albumin are decreased suggesting protein malnutrition although this may be a normal finding in the elderly.'
        elif (eta < 65) & (patientAbsAlbumin < albuminALow) & (pt < proteinALow):
            X = 'Total protein and albumin are decreased suggesting protein malnutrition.'
        elif (patientAbsAlbumin >= albuminALow) & (pt >= proteinALow) & (patientAbsAlpha1 > alpha1ALow) & (patientAbsAlpha2 < alpha2ALow) & (
                patientAbsGamma >= gammaALow) & (patientAbsGamma <= gammaAHigh):
            X = 'Alpha-2 globulins are decreased most likely due to decreased haptoglobin and/or alpha-2 macroglobulin.'
        elif (patientAbsAlbumin < albuminALow) & (pt < proteinALow) & (patientAbsGamma < gammaALow):
            X = 'Total protein, gamma globulins, and albumin are decreased suggesting protein malnutrition.'
        elif (patientAbsAlbumin > albuminALow) & (pt >= proteinALow) & (patientAbsGamma < gammaALow) & (patientAbsGamma >= 0.4):
            X = 'Gamma globulins are slightly decreased.'
        elif (patientAbsAlbumin > albuminALow) & (pt >= proteinALow) & (patientAbsGamma < 0.4) & (patientAbsGamma >= 0.2):
            X = 'Gamma globulins are moderately decreased.'
        elif (patientAbsAlbumin > albuminALow) & (pt >= proteinALow) & (patientAbsGamma < 0.2):
            X = 'Gamma globulins are markedly decreased.'
        elif (patientAbsAlbumin > albuminAHigh) & (patientAbsAlpha1 > alpha1ALow) & (patientAbsAlpha1 < alpha1RHigh) & (
                patientAbsAlpha2 > alpha2ALow) & (patientAbsAlpha2 < alpha2AHigh) & (patientAbsBeta > betaALow) & (
                patientAbsBeta < betaAHigh) & (patientAbsGamma > gammaALow) & (patientAbsGamma < gammaAHigh):
            X = 'Albumin is increased.'
        else:
            X = 'No comment available for this case.'
    return X


root = tk.Tk()
root.title('Required Information')
canvas = tk.Canvas(root, height=600, width=500)
canvas.pack()
# background_image = tk.PhotoImage(file='Desktop/landscape.png')
# background_label=tk.Label(root, image= background_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
frame = tk.Frame(root)
frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.7)
History = tk.Label(frame, text='Does this patient have a previous history?', font=20)
History.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.2)
var1 = tk.IntVar()
var1.set('no')
button_Y_H = tk.Radiobutton(root, text="Yes", font=8, variable=var1, value='yes', command=HY)
button_N_H = tk.Radiobutton(root, text="No", font=8, variable=var1, value='no', command=HN)
button_Y_H.place(relx=0.35, rely=0.25, relwidth=0.10, relheight=0.05)
button_N_H.place(relx=0.55, rely=0.25, relwidth=0.10, relheight=0.05)
Band = tk.Label(frame, text='Is there a band present in the current study?', font=20)
Band.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.2)
var2 = tk.IntVar()
var2.set('no')
button_Y_B = tk.Radiobutton(root, text="Yes", font=8, variable=var2, value='yes', command=BY)
button_N_B = tk.Radiobutton(root, text="No", font=8, variable=var2, value='no', command=BN)
button_Y_B.place(relx=0.35, rely=0.45, relwidth=0.10, relheight=0.05)
button_N_B.place(relx=0.55, rely=0.45, relwidth=0.10, relheight=0.05)
comment = tk.Text(root, height=30, width=10)
comment.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.4)
button_next = tk.Button(root, text="Next", font=8, command=nextRow)
button_next.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.05)
button_prev = tk.Button(root, text="Prev", font=8, command=prevRow)
button_prev.place(relx=0.0, rely=0, relwidth=0.1, relheight=0.05)
button_close = tk.Button(root, text="Close", font=8, command=close)
button_close.place(relx=0.45, rely=0.95, relwidth=0.1, relheight=0.05)
button_pickday = tk.Button(root, text="Pick Day", font=8, command=pickDate)
button_pickday.place(relx=0.42, rely=0, relwidth=0.16, relheight=0.05)
Date = tk.Label(frame, text='', font=20)
Date.place(relx=0.42, rely=0, relwidth=0.16, relheight=0.1)
nextRow()
root.mainloop()

