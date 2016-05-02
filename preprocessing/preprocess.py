import csv

def filter():
    outFile = open("kmeans_data.txt", "w")
    with open("twitter.csv") as csvFile:
        fileItr = csv.reader(csvFile, delimiter=',')

        for aRow in fileItr:
            try:
                interimInt = aRow[5][1:-1].split()
                interimFloat = [str(float(x)) for x in interimInt]
                interimString = ' '.join(interimFloat)
                print(interimString)
                outFile.write(interimString+"\n")
            except:
                print(interimInt)
    csvFile.close()
    outFile.close()

if __name__ == '__main__':
    filter()
