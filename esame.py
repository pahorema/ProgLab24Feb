class ExamException(Exception):
        pass

class CSVTimeSeriesFile:
    aperturafileException_str = "Oops, errore nell'apertura del file"
    chiusurafileException_str = "Oops. errore nella chiusura del file"
    nonStringException_str = "Oops, indicare il file con una stringa"


    def __init__(self, nome):
        if type(nome) is not str or not nome:
            raise ExamException(self.nonStringException_str)
        self.nome = nome

    def get_data(self):
        time_series = []
        try:
            csv_file = open(self.nome, 'r')
        except IOError:
            raise ExamException(self.aperturafileException_str)      #Eccezione in caso di errore nell'apertura del file

        for current_line in csv_file:
            try:
                line_array= current_line.split(",")
                values = [round(float(line_array[0])), float(line_array[1])]            
            except ValueError:                                      #Eccezione causata dallo split nel caso in cui ci siano altre "cose" nella riga. Bisogna ignorarla e passare alla riga successiva
                continue

            if len(time_series) > 0 and values[0] <= time_series[-1][0]:
                raise ExamException("Oops, epoch non in ordine cronologico oppure ci sono più temperature per lo stesso epoch")
            time_series.append(values)

        try:
            csv_file.close()
        except IOError:
            raise ExamException(self.chiusurafileException_str)      #Eccezione in caso di errore nella chiusura del file

        return time_series


def hourly_trend_changes(time_series):
    timeSeriesIsNotListException_str = "Oops, time_series deve essere una lista"

    if type(time_series) is not list:
        raise ExamException(timeSeriesIsNotListException_str)

    if(len(time_series) == 0):
        return time_series          #Se non c'è nessun valore non ci sarà nessuna inversione
    if(len(time_series) == 1):
        return [0]                  #Non ci sono inversioni se la lista ha solo un valore

    for line in time_series:        #Converto tutti gli epoch in ore
        line[0] = line[0]//3600


    ora_precedente = -1             #Ora utilizzata nel ciclo precedente
    crescita = False                #Tiene conto dell'aumento della temperatura
    returnValue = []                #Lista contenente il numero di inversioni

    for indice, time in enumerate(time_series[:-1]):
        if(ora_precedente != time_series[indice+1][0]):   #Controllo se sono nella stessa ora del ciclo precedente
            returnValue.append(0)                         #Aggiungo 0 alla lista delle inversioni
        ora_precedente = time_series[indice+1][0]

        if(time[1] > time_series[indice+1][1]):          #La temperatura sta scendendo?
            if(crescita):                                #Controllo per un inversione
                returnValue[-1] += 1          
            crescita = False
        if(time[1] < time_series[indice+1][1]):          #La temperatura sta aumentando?
            if (not crescita and indice != 0):
                returnValue[-1] += 1
            crescita = True
    
    return returnValue