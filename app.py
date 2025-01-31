import datetime, requests, re
from bs4 import BeautifulSoup

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return 'Hello Flask of whisk'


@app.route('/arithFormat/')
def arithmetic_Formatter():
    problemsArr = ["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]
    def eqtn_arr(eqStr):
        numOne = ''
        numTwo = ''
        operator = '+'
        dashRow = '--'
        solution = ''

        #start with checks for good equations
        #no x or / for multiplication and division
        if eqStr.find('x') != -1:
            return "Error: Operator must be '+' or '-'."
        elif eqStr.find('/') != -1:
            return "Error: Operator must be '+' or '-'."

        #next lets find both operands -> then check both are good
        if eqStr.find('+') == -1:
            operator = '-'
            numOne = eqStr[0:eqStr.find('-')].strip()
            numTwo = eqStr[eqStr.find('-') + 1:].strip()
        else:
            numOne = eqStr[0:eqStr.find('+')].strip()
            numTwo = eqStr[eqStr.find('+') + 1:].strip()
            
        #numOne and numTwo are the operands, check they contain only
        #digits and are less than 4 digits
        if len(numOne) > 4 or len(numTwo) > 4:
            return 'Error: Numbers cannot be more than four digits.'

        try:
            int(numOne)
        except ValueError:
            return 'Error: Numbers must only contain digits.'
        try:
            int(numTwo)
        except ValueError:
            return 'Error: Numbers must only contain digits.'

        #next get solution value without added spaces
        if operator == '+':
            solution = str(int(numOne) + int(numTwo))
        else:
            solution = str(int(numOne) - int(numTwo))

        #lets make dash row, and along the way add spaces to lowest num
        #and the solution
        #first need to know how wide to make dash row, need longest row
        longNumLen = 0
        #then add spaces to numOne or numTwo as needed
        if len(numOne) > len(numTwo):
            longNumLen = len(numOne)
            for i in range(0, len(numOne) - len(numTwo)):
                numTwo = ' ' + numTwo
        elif len(numOne) < len(numTwo):
            longNumLen = len(numTwo)
            for i in range(0, len(numTwo) - len(numOne)):
                numOne = ' ' + numOne
        else:
            longNumLen = len(numTwo)
            
        #no matter what we need to add dashes to dash line and
        #space(s) to the solution line
        for i in range(0, longNumLen):
            dashRow = dashRow + '-'
            if len(solution) < longNumLen + 2:
                solution = ' ' + solution
        eqtnArr = [numOne, operator, numTwo, dashRow, solution]
        #print(eqtnArr)
        return eqtnArr

    def arithmetic_arranger(problems, show_answers=False):
        #4 lines possible in formedProbs:
        topLine = ''
        operLine = ''
        dashLine = ''
        ansLine = ''
        spaceBetw = '    '

        #check if 5 or less numbers supplied
        #return error if more than 5
        if len(problems) > 5:
            return 'Error: Too many problems.'

        #now we can loop through each item efficiently
        #since we know it is under the max number
        #also check if each eqtn is ok format first with eqtn_good func
        for problem in problems:
            if isinstance(eqtn_arr(problem), str):
                return eqtn_arr(problem)
            
            #print(eqtn_arr(problem))
            #update each line based on problem output of eqtn_arr
            topLine = topLine + '  ' + eqtn_arr(problem)[0]
            operLine = operLine + eqtn_arr(problem)[1] + ' ' + eqtn_arr(problem)[2]
            dashLine = dashLine + eqtn_arr(problem)[3]
            ansLine = ansLine + eqtn_arr(problem)[4]

            #if not on last problem in array add 4 spaces to each line
            if problem != problems[len(problems) - 1]:
                topLine = topLine + spaceBetw
                operLine = operLine + spaceBetw
                dashLine = dashLine + spaceBetw
                ansLine = ansLine + spaceBetw

            #print('topLine: ' + topLine)
            #print('operLine:' + operLine)
            #print('dashLine:' + dashLine)
            #print('ansLine: ' + ansLine)

        if show_answers == False:
            print(topLine + '\n' + operLine + '\n' + dashLine)
            print('show answers false')
            return topLine + '\n' + operLine + '\n' + dashLine
        else:
            print(topLine + '\n' + operLine + '\n' + dashLine + '\n' + ansLine)
            print('show answers true')
            return topLine + '\n' + operLine + '\n' + dashLine + '\n' + ansLine

    return arithmetic_arranger(problemsArr, True)


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

@app.route("/dataAnnTest")
def data_ann_test():
    def decode_msg(docUrl):
        #parsedData will be a string featuring all characters in correct locations
        parsedData = ''
        #blank tableData array - will populate once a array of tr elements in string form are imported
        tableData = []

        #first lets send a get request to the url
        response = requests.get(docUrl)
        #next lets parse the html content of the page
        soup = BeautifulSoup(response.content, "html.parser")
        #next find the tr elements that are class c3
        rows = soup.find_all("tr")
        #then we make a for loop that goes through each of these tr element strings and pulls out the x coordinate, unicode character, and y coordinate
        for row in rows:
            #print(row)
            #get an array of string versions for each span element within this row
            cells = row.find_all("span")
            #next pull the value out of each span element and add it to a rowArr for each row
            rowArr = []
            for cell in cells:
                value = cell.get_text()
                rowArr.append(value)
                #print(str(value) + ' is the current value')
            #once we have a rowArr lets append it to our tableData arr
            tableData.append(rowArr)
            #print('new row:')
            #print(rowArr)

        #print(tableData)
        #print("above is the table")

        #now that we've pulled the in the data in the form of an array of arrays, we can remove the first array containing the column "titles" to get down to 
        #only the data we are "plotting"
        tableData.pop(0)
        #print(tableData)

        #next lets loop through the data and find the maximum x and y coordinate and add a space/period? to parsedData for each item - will replace with correct character later
        maxX = 0
        maxY = 0
        for i in range(len(tableData)):
            if int(tableData[i][0]) > maxX:
                maxX = int(tableData[i][0])
                #print('new max X Coordinate: ' + str(maxX))
            if int(tableData[i][2]) > maxY:
                maxY = int(tableData[i][2])
                #print('new max Y Coordinate: ' + str(maxY))

        #make a list of single spaces of length maxX + 1 times maxY + 1
        parsedDataList = [' '] * (maxX + 1) * (maxY + 1)

        #do a for loop as long as tableData length, replacing the space in the string at the appropriate coordinate with the current value in our table
        for i in range(len(tableData)):
            xCoord = int(tableData[i][0])
            yCoord = int(tableData[i][2])
            #calculate the linear position of the coordinate assuming before linebreaks are added and there are no "y coordinates" yet
            linearCoord = xCoord + yCoord*(maxX + 1)
            #print(linearCoord)
            parsedDataList[linearCoord] = tableData[i][1]
        
        #next make a for loop that loops for each new line, each loop pulls adds the appropriate maxX + 1 values into the string and adds a line break
        for i in range(maxY + 1):
            startIndex = 0 + i*(maxX + 1)
            endIndex = startIndex + maxX + 1
            parsedData = parsedData + ''.join(parsedDataList[startIndex:endIndex]) + '\n'

        #finally return the parsed data via parsedData
        return parsedData

    givenUrl = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
    #return decode_msg(givenUrl)
    print(decode_msg(givenUrl))
    return 'See terminal for now'